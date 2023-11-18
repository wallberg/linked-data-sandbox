#!/usr/bin/env python3

from rdflib import Dataset
from rdflib.namespace import Namespace

# For some reason, switching to ConjunctiveGraph seems to
# preserve discovered namespace prefix mapping from the
# parse(). These probably aren't necessary, but leaving
# them here for now.

PCDM = Namespace("http://pcdm.org/models#")
LDP = Namespace("http://www.w3.org/ns/ldp#")
REL = Namespace("http://id.loc.gov/vocabulary/relators/")
IANA = Namespace("http://www.iana.org/assignments/relation/")
EDM = Namespace("http://www.europeana.eu/schemas/edm/")
FEDORA = Namespace("http://fedora.info/definitions/v4/repository#")
BIBO = Namespace("http://purl.org/ontology/bibo/")

# Create a Graph
g = Dataset('BerkeleyDB')
g.open('graph')

# Print out the combined Graph in the RDF Turtle format
print(g.serialize(format="turtle"))

g.close()
