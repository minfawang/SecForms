1. Create an empty subdirectory named as 'forms'

2. Run the 'ftplib_download_forms.py' script to download all forms into the folder
	$ python ftplib_download_forms.py

3. Run the 'forms_to_one.py' script to organize all forms into one file 'all_form_idx.csv'
	$ python forms_to_one.py

4. Run the 'extract_data_from_form.py' script to extract all <f_type>-alike entries from 'all_form_idx.csv' to 'all_<f_type>_alike.csv'
	$ python extract_data_from_form.py <f_type>

	Example:
	$ python extract_data_from_form.py S-1