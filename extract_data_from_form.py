import csv
import os
def extract(args, data, out_dir, save_file=True):
	SEARCH_PATH = 'http://www.sec.gov/Archives/'

	message = '\n-------------------------------------\n'
	message += 'searching parameters:\n'
	for key, val in vars(args).items():
		if key != 'input':
			message += '{}: {}\n'.format(key, val)
	print(message)


	col_names, fin_name = args.input
	f_type = args.type
	start = args.start if args.start else '1900-01-01'
	end = args.end if args.end else '2100-01-01'
	fuzzy = args.fuzzy
	cik = args.cik


	it = col_names.find('t')
	ic = col_names.find('c')
	id = col_names.find('d')
	il = col_names.find('l')
	if it == -1 and args.type:
		raise Exception('Not found form type in document')
	if ic == -1 and args.cik:
		raise Exception('Not found cik in document')
	if id == -1 and (args.start or args.end):
		raise Exception('Not found date in document')


	args_vals = []
	for k, v in vars(args).items():
		if k != 'fuzzy' and k != 'input' and v:
			args_vals.append('{}={}'.format(k, v))
		elif k == 'fuzzy':
			args_vals.append('fuzzy=' + str(v))
		elif k == 'input':
			args_vals.append('datafile=' + v[1][:-4].replace('/', '-').replace('\\', '-'))


	num_f = 0
	data_out = []
	for row in data:
		if (ic == -1) or (not cik) or (cik == row[ic]):
			if (id == -1) or (start <= row[id] <= end):
				if (it == -1) or (not f_type) or (fuzzy and f_type in row[it]) or (f_type == row[it]):
					if SEARCH_PATH not in row[-1]:
						row[-1] = os.path.join(SEARCH_PATH, row[-1])
					data_out.append(row)
					num_f += 1

	print('search result: ')
	print("total number of rows retrieved is {}".format(num_f))

	if save_file:
		fout_name = '$'.join(args_vals) + '.csv'
		fout_name = os.path.join(out_dir, fout_name)
		write_to_file(fout_name, data_out)

	print('-------------------------------------\n')
	return data_out



def write_to_file(fout_name, data):
	with open(fout_name, "w") as fout:
		fout_content = csv.writer(fout, quotechar='\"', quoting=csv.QUOTE_NONNUMERIC, delimiter = ',')
		fout_content.writerows(data)
	print('file saved to {}'.format(fout_name))


def read_data(col_names, fin_name):
	import csv
	print('reading data from {} ...'.format(fin_name))
	with open(fin_name, "rU") as fin:
		if fin_name[-3:] == 'tsv':
			data = list(csv.reader(fin, delimiter='\t'))
		elif fin_name[-3:] == 'csv':
			data = list(csv.reader(fin))
		else:
			raise Exception('Unrecognized input file type. The program can only process csv or tsv')
		if len(data[0]) != len(col_names):
			raise Exception('Number columns not matched')

	print("finished reading data")
	return data



def set_out_dir(out_dir):
	if not os.path.isdir(out_dir):
		os.makedirs(out_dir)



if __name__ == '__main__':
	import argparse
	import os
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--input', required=True, nargs=2)
	parser.add_argument('-t', '--type', help='form type such as S-1, RW, etc.')
	parser.add_argument('-s', '--start', help='start date of search range')
	parser.add_argument('-e', '--end', help='end date of search range')
	parser.add_argument('-c', '--cik', help='cik of company')
	parser.add_argument('-f', '--fuzzy', action='store_true', help='fuzzy match string type')

	args = parser.parse_args()

	data = read_data(*args.input)

	OUT_DIR = 'search_results'
	OUT_DIR = os.path.join(os.getcwd(), OUT_DIR)
	set_out_dir(OUT_DIR)

	extract(args, data, OUT_DIR)
