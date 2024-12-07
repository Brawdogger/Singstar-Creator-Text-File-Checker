#  Singstar Creator Text File Checker
This tool is to be used alongside Singstar Creator to find any issues found within the txt files of songs that SC either doesn't find or doesn't explain clearly what the issue is. Can be very useful to use in order to troubleshoot and resolve any issues that occur during the iso creation stage (ie. SC getting indefinitely stuck whilst converting txt files).

Currently, this tools detects the following errors in text files: 
 - Txt files not using UTF-8 encoding  
 - BPM that are using a comma instead of a fullstop  
 - BPM's that are too high (above 350)  
 - Invalid Rap notes (R and G) in file  
 - (OPTIONAL - Unsure if these do cause issues) Negative timestamps on notes

For future development, the following issues still aren't being detected by the tool and need to be developed:

 - Adding checks for invalid characters within the song title and file name ( ' " / for example)
 - Check for if the song is in duet mode and if the labels are formatted correctly (Must use P1/P2 instead of DUETSINGERP1/2, ensure there aren't any spaces or other characters between P1/P2 labels)
 - Add check for if the last note of a song/duet section is a page break (Can cause singstar to crash)
 - Add check for if any notes are out of order and/or contain line breaks that occur before/during a note (Can occur commonly with songs produced with YASS)

## How to run/use
Simply download the Singstar Creator text file checker.exe and open the program. Once launched, use the "select individual files" button to select individual songs or use the "Select directory" which will automatically select all detected song text files within a directory.

Next hit the "Scan files for errors" button to scan through each file and will highlight any files that contains errors. Once scanned, this tool is also able to automatically fix any comma related errors and any incorrect file encoding by pressing the "Fix Comma & Encoding Errors" button. Any other errors detected must be manually fixed (Usually within a song editor or by downloading an alternative version of the song)

## For developers
As this project was mostly a ChatGPT hackjob, please feel free to make any improvements or changes to the code.  In order to run and make changes to this tool, please do the following:

 1. Git clone the repo
 2. Within a terminal, navigate to env/scripts and install all dependencies from the requirements file (python
pip install -r requirements.txt)
 3. Activate the virtual environment using the activate.bat script
 4. Go back to the main directory and run the main.py file
