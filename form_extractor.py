import os
import argparse
import csv
from extract_data_from_form import *

class FormExtractor:
	def __init__(self, col_names, f_search, fuzzy, f_data, out_dir):
		print('\ninitializing the form extractor ... ')
		print('file containing search parameters: {}'.format(f_search))
		self.f_search = f_search
		self.f_data = f_data
		self.it = col_names.find('t')
		self.ic = col_names.find('c')
		self.ist = col_names.find('s')
		self.ied = col_names.find('e')
		self.fuzzy = fuzzy

		self.data_columns = 't*cdl'
		self.data = self.read_data(f_data)

		self.out_dir = out_dir


	def read_data(self, fin_name):
		print('reading data from {} ...'.format(fin_name))
		with open(fin_name, "rU") as fin:
			if fin_name[-3:] == 'tsv':
				data = list(csv.reader(fin, delimiter='\t'))
			elif fin_name[-3:] == 'csv':
				data = list(csv.reader(fin))
			else:
				raise Exception('Unrecognized input file type. The program can only process csv or tsv')
			if len(data[0]) != len(self.data_columns):
				raise Exception('Number columns not matched')
		print("finished reading data")
		return data


	"""
	@param row, a list of search parameters

	Translate it into a dict of search parameters
	Example:
	row_dict = {'input': ['t*cdl', 'sample_input.tsv']
		   'type': 'S1', 
	       'start': '1990-01-01',
	       'end': '1991-01-01',
	       'cik': '832910',
	       'fuzzy': True}

	@return argparse.Namespace(**row_dict)
	"""
	def analyze_row(self, row):
		row_dict = {}
		row_dict['input'] = [self.data_columns, self.f_data]
		row_dict['type'] = row[self.it].strip() if self.it != -1 else None
		row_dict['cik'] = row[self.ic].strip() if self.ic != -1 else None
		row_dict['start'] = row[self.ist].strip() if self.ist != -1 else None
		row_dict['end'] = row[self.ied].strip() if self.ied != -1 else None
		row_dict['fuzzy'] = self.fuzzy

		return argparse.Namespace(**row_dict)

	def extract_by_row_parameters(self, row):
		row_args = self.analyze_row(row)
		matched_rows = extract(row_args, self.data, self.out_dir, save_file=False)

		rows_out = []
		for match_row in matched_rows:
			rows_out.append(row + match_row)
		return rows_out


	def extract_data(self):
		if self.f_search[-3:] == 'tsv':
			with open(self.f_search, 'rU') as fin:
				rows = list(csv.reader(fin, delimiter='\t'))
		else:
			with open(self.f_search, 'rU') as fin:
				rows = list(csv.reader(fin))

		fout_name = self.f_search[:-4] + '$results' + self.f_search[-4:]
		with open(fout_name, 'w') as fout:
			fout_writer = csv.writer(fout, quotechar='\"', quoting=csv.QUOTE_NONNUMERIC, delimiter = ',')
			for row in rows:
				rows_out = self.extract_by_row_parameters(row)
				fout_writer.writerows(rows_out)
		print('finished extracting data')
		print('file saved to {}'.format(fout_name))



def main():
	OUT_DIR = 'search_results'
	OUT_DIR = os.path.join(os.getcwd(), OUT_DIR)
	if not os.path.isdir(OUT_DIR):
		os.makedirs(OUT_DIR)

	'''
	example calling command:
	$ python form_extractor.py -s *c**tse toSearch.csv -i sample_input.tsv
	'''
	parser = argparse.ArgumentParser()
	parser.add_argument('-s', '--search', required=True, nargs=2, help='search parameters')
	parser.add_argument('-f', '--fuzzy', action='store_true', help='fuzzy match form type')
	parser.add_argument('-i', '--data_input', required=True, help='File to be searched from')

	args = parser.parse_args()
	col_names, f_search = args.search
	fuzzy = args.fuzzy
	f_data = args.data_input

	extractor = FormExtractor(col_names, f_search, fuzzy, f_data, OUT_DIR)
	extractor.extract_data()


if __name__ == '__main__':
	main()