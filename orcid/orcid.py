from pathlib import Path

from rdflib import Dataset

import requests


def query_orcid(query):
    """ Query the ORCID public API and return a set of ORCID iDs matching the query.
    """

    # Maxima for the public API
    MAX_ROWS = 1000
    MAX_START = 10000

    url = "https://pub.orcid.org/v3.0/search"
    headers = {
        "Content-type": "application/vnd.orcid+json"
    }
    params = {
        "q": query
    }

    orcid_ids = set()

    rows = MAX_ROWS
    start = 0

    while start < MAX_START:
        params['rows'] = rows
        params['start'] = start

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        results = response.json()

        count = int(results['num-found'])

        for item in results.get('result', []):
            orcid_id = item.get('orcid-identifier', {}).get('uri', '')
            if orcid_id:
                orcid_ids.add(orcid_id)

        start += rows
        if start >= count:
            break

    print(f"Found {len(orcid_ids)} ORCID iDs for query: {query}")

    return orcid_ids

# https://info.orcid.org/ufaqs/how-do-i-find-orcid-record-holders-at-my-institution/
# Accumulate ORCID iDs for UMD affiliates from different searches

orcid_ids = set()
for query in [
    'email:*@umd.edu',
    'affiliation-org-name:("University of Maryland" OR "UMD" OR "University of Maryland, College Park" OR "UMCP")',
    'ror-org-id:"https://ror.org/047s2c258"',
    'grid-org-id:"grid.164295.d"',
]:
    orcid_ids |= query_orcid(query)

print(f"Found {len(orcid_ids)} total ORCID iDs")


ds = Dataset()

g = ds.graph("https://orcid.org/")

for orcid_id, n in zip(orcid_ids, range(len(orcid_ids))):
    print(f"Processing ORCID iD: {orcid_id}")

    # ORCID Profile
    g.parse(source=orcid_id, format="turtle")

    # ORCID Works
    g.parse(source=orcid_id, format="json-ld")

    if n % 100 == 0:
        print(f"--- Processed {n} ORCID iDs ---")

ds.serialize(destination=Path("orcid.trig"), format="trig")
