#!/usr/bin/env python3

from rdflib import Graph, ConjunctiveGraph
from rdflib.term import URIRef

# Initial list of subjects to populate the graph
subjects = [
    URIRef("https://fcrepo.lib.umd.edu/fcrepo/rest/dc/2023/1/0a/d9/1a/5e/0ad91a5e-4111-45ec-aba8-42ab3651213f"),
    URIRef("https://fcrepo.lib.umd.edu/fcrepo/rest/pcdm/04/14/ef/d2/0414efd2-a519-48fd-b361-28c79082f58b"),
]

# Set of subject base patterns we are willing to follow from
# discovered objects
follows = set([
    # "https://fcrepo.lib.umd.edu/fcrepo/",
    URIRef("http://vocab.lib.umd.edu/"),
])

# Create or open a Graph with Berkeley DB persistence store
g = ConjunctiveGraph('BerkeleyDB')
g.open('graph', create=True)

print(f'Triples at start: {len(g)}')

# Document sources we have already fetched
sources = set([subject.defrag() for subject in g.subjects(predicate=None, object=None, unique=True)])

i = 0
while i < len(subjects):
    subject = subjects[i]
    source = subject.defrag()

    if source not in sources:
        # Add this source to the graph
        print(f'Adding {source=}')

        g.parse(source=source)

    # Determine if the new triples have an object which
    # we want to follow
    for _, _, object in g.triples((subject, None, None)):
        if isinstance(object, URIRef):
            newsubject = object
            if newsubject not in subjects and any(newsubject.startswith(follow) for follow in follows):
                subjects.append(newsubject)

    i += 1


print(f'Triples at end: {len(g)}')

g.close()
