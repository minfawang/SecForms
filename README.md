## Usage

1. Create an empty subdirectory named as 'forms'

2. Run the 'ftplib_download_forms.py' script to download all forms into the folder

	`$ python ftplib_download_forms.py`

3. Run the 'forms_to_one.py' script to organize all forms into one file 'all_form_idx.csv'

	`$ python forms_to_one.py`

4. Run the 'extract\_data\_from\_form.py' script
	
	For help, run
	
	`$ python extract_data_from_form.py -h`

	Some examples:

	*	`$ python extract_data_from_form.py -i t*cdl sample_input.tsv -f -t S-1 -c 35921 -s 2001-03-21 -e 2009-05-18`
		
		It will search file `sample_input.tsv` whose meanings of column names are specified as `t*cdl` and fuzzy match type `S-1` of company with CIK `35921` with publishing date starting from `2001-03-21` ending to `2009-05-18` inclusively. 
		
		Only `-i` is required argument. All other arguments are optional.

5. Run the `form_extractor.py` script

	For help, run
	
	`$ python form_extractor.py -h`
	
	Example:
	
	`python form_extractor.py -s *c**tse toSearch.csv -i sample_input.tsv`
	
	An example of `toSearch.csv` file is included.