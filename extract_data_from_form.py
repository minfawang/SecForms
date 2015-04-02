



if __name__ == '__main__':
	import csv
	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('-t', '--type', help='form type such as S-1, RW, etc.')
	parser.add_argument('-s', '--start', help='start date of search range')
	parser.add_argument('-e', '--end', help='end date of search range')
	parser.add_argument('-c', '--cik', help='cik of company')
	parser.add_argument('-f', '--fuzzy', action='store_true', help='fuzzy match string type')

	args = parser.parse_args()
	f_type = args.type
	start = args.start if args.start else '1900-01-01'
	end = args.end if args.end else '2100-01-01'
	fuzzy = args.fuzzy
	cik = args.cik
	fout_name = '_'.join(['all'] + filter(lambda x: x, vars(args).values())) + '.csv'

	with open("all_form_idx.csv", "r") as fin:
		data = list(csv.reader(fin, delimiter='\t'))
	print("finished reading data")


	num_f = 0
	with open(fout_name.format(f_type), "w") as fout:
		fout_content = csv.writer(fout, quotechar='\"', quoting=csv.QUOTE_NONNUMERIC, delimiter = ',')
		if f_type:
			for i in range(len(data)):
				if ((not cik) or (cik == data[i][2])) and (start <= data[i][3] <= end):
					if (fuzzy and f_type in data[i][0]) or (f_type == data[i][0]):
						fout_content.writerow(data[i])
						num_f += 1
		else:
			for i in range(len(data)):
				if ((not cik) or (cik == data[i][2])) and (start <= data[i][3] <= end):
						fout_content.writerow(data[i])
						num_f += 1
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
