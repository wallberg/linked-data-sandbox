#!/usr/bin/env python3


from pathlib import Path

from rdflib import Dataset, Namespace
from rdflib.namespace import RDF
from rdflib.term import URIRef, BNode

import requests
import xmltodict

SCHEMA = Namespace("http://schema.org/")
ASPACE = Namespace("https://archives.lib.umd.edu/")

ds = Dataset()
ds.bind("schema", SCHEMA)
ds.bind("aspace", ASPACE)

g = ds.graph("https://archives.lib.umd.edu/")

# Get sitemap.xml
response = requests.get("https://archives.lib.umd.edu/sitemap.xml")
data = xmltodict.parse(response.content)

for url in data['urlset']['url']:
    loc = url['loc']

    if "/resources/" in loc:
        print(loc)

        # Extract JSON-LD from this webpage and add to the graph
        g.parse(source=loc, format="json-ld", base=loc)

# Cleanup duplicate schema:PostalAddress information, per repo
for repo in g.subjects(RDF.type, URIRef(SCHEMA + "ArchiveOrganization")):

    first = True
    for address in g.objects(repo, URIRef(SCHEMA + "address")):
        if isinstance(address, BNode):
            if first:
                # Keep the first instance
                first = False
            else:
                # Delete all other instances
                g.remove((address, None, None))
                g.remove((None, None, address))

ds.serialize(destination=Path("./aspace-resources.trig"), format="trig")
