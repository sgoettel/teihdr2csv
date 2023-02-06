import os
import csv
import re
import xml.etree.ElementTree as ET

# Define the names of the columns in the CSV file
fields = [
    "letter_id",
    "file_name",
    "sender_name",
    "sender_id",
    "sender_place",
    "sender_place_id",
    "sender_place_lat",
    "sender_place_long",
    "date_sent",
    "receiver_name",
    "receiver_id",
    "receiver_place",
    "receiver_place_id",
    "receiver_place_lat",
    "receiver_place_long",
    "title",
    "url",
]

# Open a CSV file for writing
with open("teihdr_output.csv", "w") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()

    # Iterate over all XML files in the folder
    letter_id = 1
    for filename in os.listdir("xml_letters"):
        if filename.endswith(".xml"):

            tree = ET.parse(os.path.join("xml_letters", filename))
            root = tree.getroot()

            # Define the data dictionary
            data = {"letter_id": letter_id}
            data["file_name"] = filename

            # Find the <titleStmt> element
            title_stmt = root.find(".//{http://www.tei-c.org/ns/1.0}titleStmt")
            if title_stmt is None:
                print(f"Unable to extract title from {filename}")
                data["title"] = "n/a"
            else:
                title = title_stmt.find(".//{http://www.tei-c.org/ns/1.0}title")
                if title is None:
                    title = title_stmt.find(
                        ".//{http://www.tei-c.org/ns/1.0}title[@xml:lang='de']"
                    )
                if title is None:
                    title = title_stmt.find(
                        ".//{http://www.tei-c.org/ns/1.0}title[@type='main']"
                    )
                if title is None:
                    title = title_stmt.find(
                        ".//{http://www.tei-c.org/ns/1.0}title[@level='a']"
                    )
                if title is None:
                    title = title_stmt.find(
                        ".//{http://www.tei-c.org/ns/1.0}title[@level='a'][@n='1']"
                    )
                    title2 = title_stmt.find(
                        ".//{http://www.tei-c.org/ns/1.0}title[@level='a'][@n='2']"
                    )
                if title is None:
                    title = title_stmt.find(
                        ".//{http://www.tei-c.org/ns/1.0}title[@level='a'][@n='1']"
                    )
                    if title is None:
                        title = title_stmt.find(
                            ".//{http://www.tei-c.org/ns/1.0}title[@level='a'][@n='2']"
                        )
                        if title is None:
                            title = title_stmt.find(
                                ".//{http://www.tei-c.org/ns/1.0}title[@type='main']"
                            )
                            if title is None:
                                title = title_stmt.find(
                                    ".//{http://www.tei-c.org/ns/1.0}title[@xml:lang='de']"
                                )
                                if title is None:
                                    title = title_stmt.find(
                                        ".//{http://www.tei-c.org/ns/1.0}title[@n='digital']"
                                    )
                if title is not None:
                    data["title"] = re.sub(r'\s+', ' ', title.text)

                else:
                    data["title"] = "n/a"

            # Find the <publicationStmt> element
            publication_stmt = root.find(
                ".//{http://www.tei-c.org/ns/1.0}publicationStmt"
            )
            if publication_stmt is None:
                print(f"Unable to extract url from {filename}")
                data["url"] = "n/a"
            else:
                idno = publication_stmt.find(
                    ".//{http://www.tei-c.org/ns/1.0}idno[@type='URLWeb']"
                )
                if idno is not None:
                    data["url"] = idno.text
                else:
                    data["url"] = "n/a"

            # Find the <profileDesc> element
            profile_desc = root.find(".//{http://www.tei-c.org/ns/1.0}profileDesc")
            if profile_desc is None:
                print(f"Unable to extract information from profileDesc for {filename}")

                continue

            # Find the <correspDesc> element
            corresp_desc = profile_desc.find(
                ".//{http://www.tei-c.org/ns/1.0}correspDesc"
            )
            if corresp_desc is None:
                print(f"Unable to extract information from correspDesc for {filename}")
                continue
            letter_id += 1

            # Extract information from the <correspAction> elements
            for corresp_action in corresp_desc.findall(
                ".//{http://www.tei-c.org/ns/1.0}correspAction"
            ):

                type_ = corresp_action.get("type")
                if type_ == "sent":

                    pers_name = corresp_action.find(
                        ".//{http://www.tei-c.org/ns/1.0}persName"
                    )
                    if pers_name is not None:
                        forename = pers_name.findtext(
                            ".//{http://www.tei-c.org/ns/1.0}forename"
                        )
                        surname = pers_name.findtext(
                            ".//{http://www.tei-c.org/ns/1.0}surname"
                        )
                        if forename and surname:
                            data["sender_name"] = re.sub(r'\s+', ' ', f"{surname}, {forename}")
                        else:
                            data["sender_name"] = re.sub(r'\s+', ' ', pers_name.text)
                    else:
                        data["sender_name"] = "n/a"
                    data["sender_id"] = (
                        pers_name.get("ref") if pers_name is not None else "n/a"
                    )

                    place_name = corresp_action.find(
                        ".//{http://www.tei-c.org/ns/1.0}placeName"
                    )
                    data["sender_place"] = (
                        place_name.text if place_name is not None else "n/a"
                    )
                    data["sender_place_id"] = (
                        place_name.get("ref") if place_name is not None else "n/a"
                    )
                    date_element = corresp_action.find(
                        ".//{http://www.tei-c.org/ns/1.0}date"
                    )
                    if date_element is not None:
                        date_sent = date_element.get("when")
                    if date_sent is None:
                        date_sent = date_element.get("when-iso")
                    if date_sent is None:
                        date_sent = date_element.get("notBefore")
                    if date_sent is None:
                        date_sent = date_element.get("notAfter")
                    if date_sent is None:
                        date_sent = date_element.get("from")
                    if date_sent is None:
                        date_sent = date_element.text
                    data["date_sent"] = date_sent
                else:
                    pers_name = corresp_action.find(
                        ".//{http://www.tei-c.org/ns/1.0}persName"
                    )
                    if pers_name is not None:

                        forename = pers_name.findtext(
                            ".//{http://www.tei-c.org/ns/1.0}forename"
                        )
                        surname = pers_name.findtext(
                            ".//{http://www.tei-c.org/ns/1.0}surname"
                        )
                        if forename and surname:
                            data["receiver_name"] = re.sub(r'\s+', ' ', f"{surname}, {forename}")
                        else:
                            data["receiver_name"] = re.sub(r'\s+', ' ', pers_name.text)
                    else:
                        data["receiver_name"] = "n/a"
                    data["receiver_id"] = (
                        pers_name.get("ref") if pers_name is not None else "n/a"
                    )

                    place_name = corresp_action.find(
                        ".//{http://www.tei-c.org/ns/1.0}placeName"
                    )
                    data["receiver_place"] = (
                        place_name.text if place_name is not None else "n/a"
                    )
                    data["receiver_place_id"] = (
                        place_name.get("ref") if place_name is not None else "n/a"
                    )
        data = {k: v if v is not None else "n/a" for k, v in data.items()}
        writer.writerow(data)
print("Conversion complete, teihdr_output.csv file has been created.")
