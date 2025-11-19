import json
from pathlib import Path
import argparse
import time

import requests
from rdflib import Dataset

BASEURL = "https://datadryad.org"

search_url = BASEURL + "/api/v2/search"
params={
    'per_page': 100,
    'affiliation': 'https://ror.org/047s2c258',
}

ds = Dataset()

g = ds.graph("https://datadryad.org/")

# Iterate over paged results
response = requests.get(search_url, params=params)
while True:

    if not response.ok:
        print(f'Error reading response: {response}')
        break

    response = json.loads(response.text)

    for dataset in response['_embedded']['stash:datasets']:
        link = dataset['sharingLink']

        print(link)
        g.parse(source=link, format="json-ld")

    if 'next' in response['_links']:
        search_url = BASEURL + response['_links']['next']['href']
    else:
        print("Harvest complete")
        break

    print(search_url)
    response = requests.get(search_url)

    break


ds.serialize(destination=Path("dryad.trig"), format="trig")
