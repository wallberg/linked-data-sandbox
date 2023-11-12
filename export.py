#!/usr/bin/env python3

from rdflib import Graph

# Create a Graph
g = Graph('BerkeleyDB', identifier='graph')

g.open('graph', create=True)

# Print out the combined Graph in the RDF Turtle format
print(g.serialize(format="ntriples"))

g.close()
