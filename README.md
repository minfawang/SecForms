## Usage

1. Create an empty subdirectory named as 'forms'

2. Run the 'ftplib_download_forms.py' script to download all forms into the folder

	`$ python ftplib_download_forms.py`

3. Run the 'forms_to_one.py' script to organize all forms into one file 'all_form_idx.csv'

	`$ python forms_to_one.py`

4. Run the 'extract_data_from_form.py' script
	
	For help, run
	
	`$ python extract_data_from_form.py -h`

	Some examples:

	*	`$ python extract_data_from_form.py -f -t S-1 -c 35921 -s 2001-03-21 -e 2009-05-18`
		
		It will fuzzy match type `S-1` of company with CIK `35921` with publishing date starting from `2001-03-21` ending to `2009-05-18` inclusively. 

	*	`$ python extract_data_from_form.py`
		
		It will fetch all entires to an output file!! Please be cautious calling the program with no arguments.