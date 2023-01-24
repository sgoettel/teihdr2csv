import csv
import requests
import re


def get_coordinates(place_id):
    url = f"https://sws.geonames.org/{place_id}/about.rdf"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Parse the XML content of the response
            xml_content = response.content
            xml_content = xml_content.decode()
            # Extract the latitude and longitude coordinates
            lat_match = re.search(
                r"<wgs84_pos:lat>([^<]+)</wgs84_pos:lat>", xml_content
            )
            long_match = re.search(
                r"<wgs84_pos:long>([^<]+)</wgs84_pos:long>", xml_content
            )
            if lat_match and long_match:
                lat = lat_match.group(1)
                long = long_match.group(1)
                return (lat, long)
            else:
                print(f"Could not find coordinates for place ID {place_id}")
        else:
            print(f"Error getting coordinates for place ID {place_id}")
    except requests.exceptions.RequestException as e:
        print(f"Error getting coordinates for place ID {place_id}: {e}")


def main():
    row_counter = 0
    with open("teihdr_output.csv", "r") as file:
        reader = csv.reader(file)
        header = next(reader)  # save the header
        data = []
        for i, row in enumerate(reader):
            (
                letter_id,
                file_name,
                sender_name,
                sender_id,
                sender_place,
                sender_place_id,
                sender_place_lat,
                sender_place_long,
                date_sent,
                receiver_name,
                receiver_id,
                receiver_place,
                receiver_place_id,
                receiver_place_lat,
                receiver_place_long,
                title,
                url,
            ) = row

            if sender_place_id and sender_place_id.startswith(
                "https://www.geonames.org"
            ):
                place_id = sender_place_id.split("/")[-1]
                lat, long = get_coordinates(place_id)
                if lat is not None and long is not None:
                    if row[6] in ("n/a", ""):
                        row[6] = lat
                    if row[7] in ("n/a", ""):
                        row[7] = long
            elif sender_place_id:
                print(f"Invalid sender place ID {sender_place_id} in row {i+1}")
                row[6] = ""
                row[7] = ""
            else:
                row[6] = ""
                row[7] = ""

            if receiver_place_id and receiver_place_id.startswith(
                "https://www.geonames.org"
            ):
                place_id = receiver_place_id.split("/")[-1]
                lat, long = get_coordinates(place_id)
                if lat is not None and long is not None:
                    if row[13] in ("n/a", ""):
                        row[13] = lat
                    if row[14] in ("n/a", ""):
                        row[14] = long
            

            data.append(row)
    with open("teihdr_output.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)


if __name__ == "__main__":
    main()