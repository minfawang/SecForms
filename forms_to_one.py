import csv
import os
from glob import glob

form_dir = "forms"
dest_file_name = "all_form_idx.tsv"
with open(dest_file_name, "w") as fout:
	fout_content = csv.writer(fout, quotechar='\"', quoting=csv.QUOTE_NONNUMERIC, delimiter = '\t')
	for form_name in glob(os.path.join(form_dir, "*.txt")):
		with open(form_name, "r") as form_file:
			start_parsing = False
			for line in form_file:
				line = line.strip()
				if start_parsing:
					# check valid line
					if line[:5] == "-----":
						continue
					if len(line) > cell_indexes[4]: 
						row = []
						row.append(line[cell_indexes[0]:cell_indexes[1]].strip())
						row.append(line[cell_indexes[1]:cell_indexes[2]].strip())
						row.append(line[cell_indexes[2]:cell_indexes[3]].strip())
						row.append(line[cell_indexes[3]:cell_indexes[4]].strip())
						row.append(line[cell_indexes[4]:               ].strip())
						fout_content.writerow(row)

				else:
					if line.startswith("Form Type"):
						cell_indexes = []
						cell_indexes.append(line.find("Form Type"))
						cell_indexes.append(line.find("Company Name"))
						cell_indexes.append(line.find("CIK"))
						cell_indexes.append(line.find("Date Filed"))
						cell_indexes.append(line.find("File Name"))
						start_parsing = True

