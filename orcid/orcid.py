from pathlib import Path

from rdflib import Dataset

import requests

CACHE_DIR = Path.home() / "git" / "linked-data-sandbox" / ".cache" / "orcid"

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
    'affiliation-org-name:("UMD" OR "University of Maryland, College Park" OR "UMCP")',
    'ror-org-id:"https://ror.org/047s2c258"',
    'grid-org-id:"grid.164295.d"',
]:
    orcid_ids |= query_orcid(query)

print(f"Found {len(orcid_ids)} total ORCID iDs")


ds = Dataset()

g = ds.graph("https://orcid.org/")

# Download each ORCID iD, caching results so the
# process is restartable (due to long download times)
CACHE_DIR.mkdir(parents=True, exist_ok=True)
orcid_ids = sorted(orcid_ids)
for orcid_id, n in zip(orcid_ids, range(len(orcid_ids))):
    cache_file = CACHE_DIR / f"{orcid_id[18:]}.trig"

    if cache_file.exists():
        print(f"Skipping cached ORCID iD: {orcid_id}")

    else:
        print(f"Downloading ORCID iD: {orcid_id}")

        try:
            # ORCID Profile
            g.parse(source=orcid_id, format="turtle")

            # ORCID Works
            g.parse(source=orcid_id, format="json-ld")

            ds.serialize(destination=cache_file, format="trig")

        except Exception as e:
            print(f"Error serializing ORCID iD {orcid_id}: {e}")

            # Remove the malformed cache file if it exists
            cache_file.unlink(missing_ok=True)

        # Clear the graph
        for s, p, o in list(g):
            g.remove((s, p, o))

    if n % 99 == 0:
        print(f"--- Completed {n+1} ORCID iDs ---")

# Combine cached files into final dataset
for cache_file in CACHE_DIR.glob("*.trig"):
    g.parse(source=cache_file, format="trig")

ds.serialize(destination=Path("orcid.trig"), format="trig")
