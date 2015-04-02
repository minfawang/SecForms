import requests
from bs4 import BeautifulSoup
import time
import os
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
# from splinter import Browser


# browser = Browser()
# url = "ftp://ftp.sec.gov/edgar/full-index/2014/QTR1/form.idx"
search_url = "ftp://ftp.sec.gov/edgar/full-index/"
cachedir = "/Users/voiceup/Desktop"
form_dir = "forms/"
TRYING_TIMES = 3


def get_browser(cachedir):
	profile = webdriver.FirefoxProfile()
	profile.set_preference('browser.download.folderList', 2)
	profile.set_preference('browser.download.dir', cachedir)
	profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/pdf, text/plain, application/vnd.idx')
	profile.set_preference('plugin.disable_full_page_plugin_for_types', 'application/pdf, text/plain, application/vnd.idx')
	profile.set_preference('browser.helperApps.alwaysAsk.force', False)
	profile.set_preference('browser.download.manager.showWhenStarting', False)
	profile.set_preference('pdfjs.disabled', True)
	return webdriver.Firefox(profile)

def write_content(page_source, file_path):
	soup = BeautifulSoup(page_source)
	form_content = soup.find_all("body")[0].text

	print("getting {}".format(file_path))

	with open(file_path, "w") as f_out:
		f_out.write(form_content.encode('utf-8'))


browser = get_browser(cachedir)
browser.get(search_url)
soup = BeautifulSoup(browser.page_source)
year_dirs = soup.find_all("a", {"class": "dir"})

if not os.path.isdir(form_dir):
	os.makedirs(form_dir)

# year0 = year_dirs[0]
# link0 = year0["href"]
# link0 = os.path.join(search_url, link0)
# browser.get(link0)
for year_dir in year_dirs:
	year = year_dir["href"].replace("/", "")
	year_dir = os.path.join(search_url, year)
	print("year {}".format(year))

	for i in range(TRYING_TIMES):
		try:
			browser.get(year_dir)
			time.sleep(1)
			soup = BeautifulSoup(browser.page_source)
			qtr_dirs = soup.find_all("a", {"class": "dir"})
			break
		except:
			try: 
				WebDriverWait(browser, 1).until(EC.alert_is_present())
				alert = browser.switch_to_alert()
				alert.accept()
			except TimeoutException:
				pass



	for qtr_dir in qtr_dirs:
		qtr = qtr_dir["href"].replace("/", "")
		qtr_dir = os.path.join(year_dir, qtr)

		file_name = year + "_" + qtr + ".txt"
		file_path = os.path.join(form_dir, file_name)
		if os.path.exists(file_path):
			print("skip {}".format(file_path))
			continue

		for i in range(TRYING_TIMES):
			try: 
				browser.get(qtr_dir)
				break
			except:
				try: 
					WebDriverWait(browser, 1).until(EC.alert_is_present())
					alert = browser.switch_to_alert()
					alert.accept()
				except TimeoutException:
					pass

		for i in range(TRYING_TIMES):
			try:
				form_element = browser.find_element_by_link_text("form.idx")
				form_element.click()
				break
			except:
				try:
					WebDriverWait(browser, 1).until(EC.alert_is_present())
					alert = browser.switch_to_alert()
					alert.accept()
				except TimeoutException:
					pass

		for i in range(TRYING_TIMES):
			try:
				write_content(browser.page_source, file_path)
				break
			except:
				try:
					WebDriverWait(browser, 1).until(EC.alert_is_present())
					alert = browser.switch_to_alert()
					alert.accept()
				except TimeoutException:
					pass



		# MAX_WAIT_TIME = 5
		# for i in range(MAX_WAIT_TIME):
			# try:
			# 	write_content(browser.page_source, form_dir, year, qtr)				
			# 	break
			# except:
			# 	alert = browser.switch_to_alert()
			# 	alert.accept()
			# 	print("alert accepted")
			# 	time.sleep(1)

		# write content

	# print("length of year_dirs: {}".format(len(year_dirs)))




time.sleep(2)
browser.quit()
