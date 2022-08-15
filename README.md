# GDB-XLSX Comparer
This tool compares a gdb model against an xlsx file.
### Usage
Clone the repository and cd into it. 

Activate the virtual environment with ```source myenv/bin/activate```
Alternatively, install the required dependency packages with ```python3 -m pip install -r requirements.txt```. You may need to install your platform-specific version of the GDAL library.

If the gdb and xlsx have identical columns but with differing names (e.g "PSTL_CDE" in the gdb and "Postal Code" in the xlsx are both referring to the same contents), update the provided mappings.config accordingly.

Then, run the program with```python3 main.py```. A GUI window should appear.
Click the "Browse" buttons to navigate and select the gdb file, the xlsx file and the directory where you wish the report output to be generated in. 
Type in the name of any one uniquely identifying field under "Key". (for e.g if for the column "UNIQ_ID", every single entry has a unique field, type "UNIQ_ID" into Key)
Then, click "Analyze + Download"
The report csv will be generated and saved with the name ```report_xxxxxxx.txt``` in the current directory.
