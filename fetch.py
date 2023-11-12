#!/usr/bin/env python3

from rdflib import Graph

sources = [
    "https://fcrepo.lib.umd.edu/fcrepo/rest/dc/2023/1/0a/d9/1a/5e/0ad91a5e-4111-45ec-aba8-42ab3651213f",
    "https://fcrepo.lib.umd.edu/fcrepo/rest/pcdm/04/14/ef/d2/0414efd2-a519-48fd-b361-28c79082f58b",
    "http://vocab.lib.umd.edu/form#records",
    "http://vocab.lib.umd.edu/collection#0068-LBR-RG9-003",
]

# Create a Graph
g = Graph('BerkeleyDB', identifier='graph')

g.open('graph', create=True)
print(f'{len(g)=}')

for source in sources:

    q = f"""
    SELECT ?o
    WHERE {{
        <{source}> ?p ?o .
    }}
"""
    # print(q)

    # Apply the query to the graph and iterate through results

    in_graph = False
    for r in g.query(q):
        in_graph = True
        break

    if not in_graph:
        print(f'Adding {source=}')
        g.parse(source=source)

print(f'{len(g)=}')

# Print out the combined Graph in the RDF Turtle format
# print("---------------")
# print(g.serialize(format="turtle"))

# Query the data in g using SPARQL
# This query returns the 'name' of all ``foaf:Person`` instances
q = """
    SELECT ?s ?p ?o
    WHERE {
        ?s ?p ?o .
    }
"""

# Apply the query to the graph and iterate through results
for r in g.query(q):
    print(r)

g.close()
