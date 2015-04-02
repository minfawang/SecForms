import os
import ftplib

form_dir = "forms/"

ftp = ftplib.FTP('ftp.sec.gov', 'anonymous')

for year in range(1993, 2015):
    for qtr in range(1, 5):
        url = "edgar/full-index/{year}/QTR{qtr}/form.idx".format(year=year, qtr=qtr)
        filename = "{year}_{qtr}.txt".format(year=year, qtr=qtr)

        print "Process URL: " + url

        # manually download the file
        with open(os.path.join(form_dir, filename), "wb") as file:
            ftp.retrbinary("RETR " + url, file.write)

ftp.close()