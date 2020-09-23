# estc-xml2csv

## Contents

This repo contains the estc_xml2csv-function inside the likewise-named python script. The function converts the xml-format estc into a csv-format estc.
To use the the function to convert the xml to csv, do the following:

1) (optional) Add the estc_xml -file or symbolic link to this repo locally.
   As of 9/2020 we used github/comhis/estc-data-originals/estc-xml-raw/ESTC0920.xml
2) Open the script Estc_xml2csv.py and define the input_xml = "estc.xml" (change XML file name path as needed)
3) Run the script Estc_xml2csv.py modified in this manner on command line with "python3 Estc_xml2csv.py"

Then manually copy the parsed CSV file into github/comhis/estc-data-originals/estc-csv-raw/

## TODO

 1. Automate the process better
 2. Consider moving this script to the github/comhis/estc-data-originals repository, so it can be better automated.

## Troubleshoot:

  1. The print command of the script Estc_xml2csv.py at the line 58 might need parentheses around it (might also be a local problem - Iiro). Add them if running the script fails.

  2. Encoding problems can cause failure. Adding errors='ignore' to the open-command of Estc_xml2csv.py at the line 20 solves this,
but this should not be done for the final run of the script, doing this loses information. The specification of the
encoding-parameter also affects the number of failiors, but such that caused 0 erros on windows was not found - Iiro, 22.9.2020. 

