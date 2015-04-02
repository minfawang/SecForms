# When I wrote the script of attach_sic.py. There are minor errors that 
# sometime it doesn't get the right sic, but get the city name
import csv
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('fin', help='input file to correct')
args = parser.parse_args()

fin_name = args.fin
with open(fin_name, 'r') as fin:
	data = list(csv.reader(fin))

with open(fin_name, 'w') as fout:
	csv_writer = csv.writer(fout)
	for row in data:
		if all(c.isdigit() for c in row[5]):
			csv_writer.writerow(row)
		else:
			csv_writer.writerow(row[:5] + [''])