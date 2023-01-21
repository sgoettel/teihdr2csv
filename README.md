# teihdr2csv
A Python script for extracting data from letters in TEI 


# letter_data.py

This script extracts data from TEI-encoded letter files in XML format and writes the data to a CSV file. The script is designed to work specifically with letter files that are encoded according to the guidelines of the Text Encoding Initiative (TEI).

## Input

The script takes as input a directory containing TEI-encoded letter files in XML format. The directory should be named `xml_letters` and should be located in the same directory as the script. The script will iterate through all files in the directory that have the `.xml` file extension.

The script extracts data from the following elements and attributes within the XML files:

-   `<persName>`: The script extracts the text of the element, representing the name of the person, and the `ref` attribute, representing the ID of the person in a certain reference system (e.g. GND ID)
-   `<placeName>`: The script extracts the text of the element, representing the name of the place, and the `ref` attribute, representing the ID of the place in a certain reference system (e.g. GND ID)
-   `<date>`: The script extracts the `when`, `notBefore` or `notAfter` attribute, representing the date the letter was sent or received
-   `correspAction`: The script extracts the `type` attribute, representing whether the letter was sent or received, and uses it to determine which data belongs to the sender or receiver.


## Output

The script outputs a CSV file named `letters.csv` in the same directory as the script. The file contains a table with the following columns:

-   `letter_id`: An incrementing ID number for each letter
-   `sender_or_receiver`: Whether the data belongs to the sender or receiver
-   `sender_name`: The name of the sender
-   `sender_id`: The ID of the sender in a certain reference system (e.g. GND ID)
-   `sender_place`: The name of the place the letter was sent from.
-   `sender_place_id`: The ID of the place the letter was sent from in the form of a URL.
-   `date_sent`: The date the letter was sent.
-   `receiver_name`: The name of the receiver of the letter.
-   `receiver_id`: The ID of the receiver of the letter in the form of a URL.
-   `receiver_place`: The name of the place the letter was sent to.
-   `receiver_place_id`: The ID of the place the letter was sent to in the form of a URL.
-    `title`: The title of the letter, extracted from the TEI header using a series of specific criteria in the following order: <title> element with no attributes, <title xml:lang="de">, <title type="main">, <title level="a">, <title level="a" n="1">, <title level="a" n="2">, <title n="digital">
-   `url`: The URL of the letter, extracted from the TEI header using the <publicationStmt> element and the <idno type="URLWeb"> element
-   `file_name`: The name of the file that the script iterated through, taken from the "xml_letters" folder.

The script only writes rows to the CSV file if it is able to extract information from the corresponding XML file. If the script is unable to extract information from an XML file, it prints a message to the console indicating the name of the file.

The script fills in the missing information with "n/a" in the CSV file if it's not able to extract it from the XML file.
