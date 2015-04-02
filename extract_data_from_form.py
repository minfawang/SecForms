import csv
import argparse

with open("all_form_idx.csv", "r") as fin:
	data = list(csv.reader(fin, delimiter='\t'))
print("finished reading data")



if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('f_type', help='form type such as S-1, RW, etc.')
	args = parser.parse_args()
	f_type = args.f_type

	num_f = 0
	with open("all_{}_alike.csv".format(f_type), "w") as fout:
		fout_content = csv.writer(fout, quotechar='\"', quoting=csv.QUOTE_NONNUMERIC, delimiter = ',')
		for i in range(len(data)):
			if f_type in data[i][0]:
				fout_content.writerow(data[i])
				num_f += 1
	print("total number of S-1 alike is {}".format(num_f))








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
