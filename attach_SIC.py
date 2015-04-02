import requests
import bs4
import csv
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('fin', help='input file')

args = parser.parse_args()
fin_name = args.fin
fout_name = fin_name.replace('.', '_sic.')

with open(fin_name, 'r') as f_in:
	data = list(csv.reader(f_in))

num_row_processed = 0
with open(fout_name, 'w') as f_out:
	csv_writer = csv.writer(f_out, quoting=csv.QUOTE_NONNUMERIC, quotechar='\"')
	for row in data:
		try:
			CIK = row[2]
			dest_url = 'http://www.sec.gov/cgi-bin/browse-edgar?CIK={}&Find=Search&owner=exclude&action=getcompany'.format(CIK)

			r = requests.get(dest_url)
			soup = bs4.BeautifulSoup(r.text)
			sic = soup.find('p', {'class': 'identInfo'}).find('a').text
			if all(c.isdigit() for c in sic):
				row.append(sic)
			else:
				row.append('')
		except:
			print('Error on CIK = {}'.format(CIK))
			row.append('')

		csv_writer.writerow(row)

		num_row_processed += 1
		if num_row_processed % 20 == 0:
			print('Processed {} rows'.format(num_row_processed))