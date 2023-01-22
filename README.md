# teihdr2csv

This script extracts data about the sender and receiver from TEI-encoded letter files in XML format and writes the data to a CSV file. The script is designed to work specifically with letter files that are encoded according to the guidelines of the Text Encoding Initiative (TEI).

## Usage

To run the script, you need to have Python 3 installed on your machine. The directory should be named `xml_letters` and should be located in the same directory as the script. The script is using the [xml.etree.ElementTree](https://docs.python.org/3/library/xml.etree.elementtree.html) and [csv](https://docs.python.org/3/library/csv.html) modules which are built-in modules in Python.

`$ python3 teihdr2csv.py`

If you want to change the name of the output file or the path of the output file, you can change it in the script.

## Input

The script takes as input a directory containing TEI-encoded letter files in XML format. The directory should be named `xml_letters` and should be located in the same directory as the script. The script will iterate through all files in the directory that have the `.xml` file extension. If you want to change the name of the output file or the path of the output file, you can change it in the script.

The script extracts data from the following elements and attributes within the XML files from the sender and the receiver:

-   `<persName>`: The script extracts the text of the element <forename> and <surname>, or just <persName>, representing the name of the person, and the `ref` attribute, representing the ID of the person in a certain reference system (e.g. GND, Wikidata)
-   `<placeName>`: The script extracts the text of the element, representing the name of the place, and the `ref` attribute, representing the ID of the place in a certain reference system (e.g. GeoNames)
-   `<date>`: The script extracts the `when(-iso)`, `notBefore` or `notAfter` attribute, representing the date the letter was sent or received. If none of these attributes are found, the script will get the text content of the `<date>` element as a fallback.
-   `correspAction`: The script extracts the `type` attribute, representing whether the letter was sent or received, and uses it to determine which data belongs to the sender or receiver.
-   `<titleStmt>`: The script looks for the `<title>` tags within the `<titleStmt>` element in the XML files. If a `<title>` element is found, and it does not have any attributes, the script takes the text content of that element as the title of the letter and writes it to the "title" column in the CSV file. If no such `<title>` element is found, the script then looks for a different @type attribute e.g.:  `<title xml:lang="de">`,  `<title type="main">`,  `<title level="a">` etc. If none of these elements are found, the script will write "n/a" to the "title" column in the CSV file.
-   `<publicationStmt>`: The script extracts the text content of the `<publicationStmt>` element. This could be a link to a digitized version of the letter on a library's website. If the <publicationStmt> element is not present in the XML file, the script will assign the value "n/a" to the corresponding field in the output CSV.

The script then writes the extracted data to a CSV file named `teihdr_output.csv` in the same directory as the script.

## Output

The script outputs a CSV file named `letters.csv` in the same directory as the script. The file contains a table with the following columns:

-   `letter_id`: An incrementing ID number for each letter
-   `file_name` : The name of the input file(s) from the folder "xml_letters"
-   `sender_name`: The name of the sender
-   `sender_id`: The ID of the sender in a certain reference system (e.g. GND ID)
-   `sender_place`: The name of the place the letter was sent from.
-   `sender_place_id`: The ID of the place the letter was sent from in the form of a URL.
-   `date_sent`: The date the letter was sent.
-   `receiver_name`: The name of the receiver of the letter.
-   `receiver_id`: The ID of the receiver of the letter in the form of a URL.
-   `receiver_place`: The name of the place the letter was sent to.
-   `receiver_place_id`: The ID of the place the letter was sent to in the form of a URL.
-   `title`: The title of the letter
-   `url`: The URL of the letter if it is available

`teihdr2csv.py` only writes rows to the CSV file if it is able to extract information from the corresponding XML file. If the script is unable to extract information from an XML file, it prints a message to the console indicating the name of the file.

The script fills in the missing information with "n/a" in the CSV file if it's not able to extract certain data from the XML file.

The script will overwrite the existing `letters.csv` file if it already exists in the same directory as the script. If you want the script to add new data to the existing file, you need to open the file in "append" mode instead of "write" mode. To do this, you can change this line:

`with open("letters_test.csv", "w") as csvfile:` 

to

`with open("letters_test.csv", "a") as csvfile:` 

This way, every time the script is run, it will add new data to the existing file, rather than overwriting the whole file.
 
## Add latitude and longitude for the place of sender/receiver
  
teihdr2csv also creates columns named `place_lat` and `place_long` for each the sender and receiver. In order to be able to use the function of extracting the coordinates as well, the script "geonames_coordinates.py" must be executed after creating the csv file. The script currently only works with GeoNames URLs. The script uses the `sender_place_id` and `receiver_place_id` columns in the CSV file, which contain the place IDs in the GeoNames reference system (e.g. [https://www.geonames.org/2657896](https://www.geonames.org/2657896)). It then calls the GeoNames web service to retrieve the latitude and longitude coordinates for each place ID, and adds these coordinates to the `sender_place_lat` and `sender_place_long` or `receiver_place_lat` and `receiver_place_long` columns in the CSV file.
  
To get the latitude and longitude values, the script must be located in the same directory as the "teihdr_output.csv" file:
  `$ python3 geonames_coordinates.py`
  
If you should have noticed any errors or if you have any additions, comments or suggestions for improvement, please feel free to send me a message.

