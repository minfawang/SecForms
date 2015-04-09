



if __name__ == '__main__':
	import csv
	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--input', required=True, nargs=2)
	parser.add_argument('-t', '--type', help='form type such as S-1, RW, etc.')
	parser.add_argument('-s', '--start', help='start date of search range')
	parser.add_argument('-e', '--end', help='end date of search range')
	parser.add_argument('-c', '--cik', help='cik of company')
	parser.add_argument('-f', '--fuzzy', action='store_true', help='fuzzy match string type')


	args = parser.parse_args()
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
		raise Exception('Nout found date in document')


	args_vals = []
	for k, v in vars(args).items():
		if k != 'fuzzy' and k != 'input':
			args_vals.append(v)
		elif k == 'fuzzy' and v:
			args_vals.append('fuzzy')
		elif k == 'input':
			args_vals.append(v[1][:-4].replace('/', '-').replace('\\', '-'))

	fout_name = '_'.join(['all'] + filter(lambda x: x, args_vals)) + '.csv'


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


	num_f = 0
	with open(fout_name.format(f_type), "w") as fout:
		fout_content = csv.writer(fout, quotechar='\"', quoting=csv.QUOTE_NONNUMERIC, delimiter = ',')
		# if f_type:
		for i in range(len(data)):
			if (ic == -1) or (not cik) or (cik == data[i][ic]):
				if (id == -1) or (start <= data[i][id] <= end):
					if (it == -1) or (not f_type) or (fuzzy and f_type in data[i][it]) or (f_type == data[i][it]):
						fout_content.writerow(data[i])
						num_f += 1
		# else:
		# 	for i in range(len(data)):
		# 		if ((not cik) or (cik == data[i][2])) and (start <= data[i][3] <= end):
		# 				fout_content.writerow(data[i])
		# 				num_f += 1
	print("total number of rows retrieved is {}".format(num_f))
	print('file saved to {}'.format(fout_name))








# num_RW = 0
# # with open("all_RW.csv", "w") as fout:
# with open("all_RW_alike.csv", "w") as fout:
# 	fout_content = csv.writer(fout, quotechar='\"', quoting=csv.QUOTE_NONNUMERIC, delimiter = ',')
# 	for i in range(len(data)):
# 		# if data[i][0] == 'RW':
# 		if 'RW' in data[i][0]:
# 			fout_content.writerow(data[i])
# 			num_RW += 1
# print("total number of RW is {}".format(num_RW))


# num_RW = 0
# with open("all_10K_10Q_8K.csv", "w") as fout:
# 	fout_content = csv.writer(fout, quotechar='\"', quoting=csv.QUOTE_NONNUMERIC, delimiter = ',')
# 	for i in range(len(data)):
# 		form_type = data[i][0]
# 		if form_type == '10-K' or form_type == '10-Q' or form_type == '8-K':
# 			fout_content.writerow(data[i])
# 			num_RW += 1
# print("total number of 10K, 10Q, 8K is {}".format(num_RW))
