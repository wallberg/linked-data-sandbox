from pathlib import Path

from rdflib import Dataset, Namespace
from rdflib.namespace import RDF
from rdflib.term import URIRef, BNode

import requests


def query_wikidata(sparql_query):
    url = "https://query.wikidata.org/sparql"
    headers = {
        "Accept": "application/sparql-results+json"
    }
    params = {
        "query": sparql_query
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    results = response.json()
    return results


# Example usage
sparql_query = """
SELECT DISTINCT ?item ?itemLabel ?itemDescription
WHERE {
    ?item wdt:P485 wd:Q7895690. # Anything with archives at University of Maryland Libraries

    SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }

}
"""

results = query_wikidata(sparql_query)
# print(json.dumps(results, indent=2))

SCHEMA = Namespace("http://schema.org/")
ASPACE = Namespace("https://archives.lib.umd.edu/")

ds = Dataset()
ds.bind("schema", SCHEMA)
ds.bind("aspace", ASPACE)

g = ds.graph("https://www.wikidata.org/")

for binding in results['results']['bindings']:
    item = binding.get('item', {}).get('value', '')
    entity = item.split('/')[-1]  # Extract entity ID from URL
    ttl_url = f"https://www.wikidata.org/wiki/Special:EntityData/{entity}.ttl"
    print(ttl_url)
    g.parse(source=ttl_url, format="turtle")

ds.serialize(destination=Path("./wikidata.trig"), format="trig")
