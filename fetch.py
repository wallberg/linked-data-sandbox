#!/usr/bin/env python3

from rdflib import Graph

sources = [
    "https://fcrepo.lib.umd.edu/fcrepo/rest/dc/2023/1/0a/d9/1a/5e/0ad91a5e-4111-45ec-aba8-42ab3651213f",
    "https://fcrepo.lib.umd.edu/fcrepo/rest/pcdm/04/14/ef/d2/0414efd2-a519-48fd-b361-28c79082f58b",
    "http://vocab.lib.umd.edu/form#records",
    "http://vocab.lib.umd.edu/collection#0068-LBR-RG9-003",
]

# Create or open a Graph with Berkeley DB persistence store
g = Graph('BerkeleyDB', identifier='graph')

g.open('graph', create=True)
print(f'Triples at start: {len(g)}')

for source in sources:

    # Determine if this source already exists in the graph
    q = f"""
    SELECT ?o
    WHERE {{
        <{source}> ?p ?o .
    }}
"""

    in_graph = False
    for r in g.query(q):
        in_graph = True
        break

    if not in_graph:
        # Add this source to the graph
        print(f'Adding {source=}')

        g.parse(source=source)

print(f'Triples at end: {len(g)}')

g.close()
