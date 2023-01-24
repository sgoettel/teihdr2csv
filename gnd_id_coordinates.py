import csv
import re
import requests

def extract_id(url):
    match = re.search(r'gnd/(\d+-\d+)', url)
    return match.group(1)

def get_coordinates(id):
    url = f'http://hub.culturegraph.org/entityfacts/{id}'
    response = requests.get(url)
    data = response.json()
    coordinates = data['location']['geometry']['coordinates']
    return coordinates

def update_csv(file_name):
    with open(file_name, 'r', newline='') as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    for row in rows:
        if row['sender_place_id'].startswith('https://d-nb.info/gnd/') or row['sender_place_id'].startswith('http://d-nb.info/gnd/'):
            id = extract_id(row['sender_place_id'])
            coordinates = get_coordinates(id)
            if row.get('sender_place_lat','') in ("n/a",''):
                row['sender_place_lat'] = coordinates[1]
            if row.get('sender_place_long','') in ("n/a",''):
                row['sender_place_long'] = coordinates[0]
        if row['receiver_place_id'].startswith('https://d-nb.info/gnd/') or row['receiver_place_id'].startswith('http://d-nb.info/gnd/'):
            id = extract_id(row['receiver_place_id'])
            coordinates = get_coordinates(id)
            if row.get('receiver_place_lat','') in ("n/a",''):
                row['receiver_place_lat'] = coordinates[1]
            if row.get('receiver_place_long','') in ("n/a",''):
                row['receiver_place_long'] = coordinates[0]

    with open(file_name, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(rows)

# usage example:
file_name = 'teihdr_output.csv'
update_csv(file_name)