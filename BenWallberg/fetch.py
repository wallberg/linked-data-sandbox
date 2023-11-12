#!/usr/bin/env python3

from rdflib import Graph

sources = [
    ("turtle", "https://wallberg.solidcommunity.net/profile/card#me"),
    ("turtle", "https://orcid.org/0000-0002-4904-005X"),
    ("json-ld", "https://orcid.org/0000-0002-4904-005X"),
]

# Create a Graph
g = Graph()

for format, source in sources:

    print(f'Parsing {format=}, {source=}')
    g.parse(format=format, source=source)

# Print out the combined Graph in the RDF Turtle format
print("---------------")
print(g.serialize(format="turtle"))

# Query the data in g using SPARQL
# This query returns the 'name' of all ``foaf:Person`` instances
q = """
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>

    SELECT ?name
    WHERE {
        ?p rdf:type foaf:Person .

        ?p foaf:name ?name .
    }
"""

# Apply the query to the graph and iterate through results
for r in g.query(q):
    print(r["name"])
