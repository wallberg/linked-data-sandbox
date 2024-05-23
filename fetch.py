#!/usr/bin/env python3

from os import path

from rdflib import plugin, Dataset
from rdflib.term import URIRef
from rdflib.store import Store

# Initial list of subjects to populate the graph
subjects = [
    (URIRef("https://www.wikidata.org/entity/Q7730092"), None),
    (URIRef("https://drum.lib.umd.edu/items/f4d2184d-4bde-46aa-8477-25e8605c8cc4"), "json-ld"),
    (URIRef("https://fcrepo.lib.umd.edu/fcrepo/rest/dc/2023/1/0a/d9/1a/5e/0ad91a5e-4111-45ec-aba8-42ab3651213f"), None),
    (URIRef("https://fcrepo.lib.umd.edu/fcrepo/rest/pcdm/04/14/ef/d2/0414efd2-a519-48fd-b361-28c79082f58b"), None),
]

# Set of subject base patterns we are willing to follow from
# discovered objects
follows = set([
    # "https://fcrepo.lib.umd.edu/fcrepo/",
    URIRef("http://vocab.lib.umd.edu/"),
])

# Create or open a Graph with Level DB persistence store
store = plugin.get("LevelDB", Store)(identifier=URIRef("ld-sandbox"))

dbpath = "./storedb"
create = not path.exists(dbpath)

g = Dataset(store)
g.open(dbpath, create=create)

print(f'Triples at start: {len(g)}')

# Document sources we have already fetched
sources = set([
    subject.defrag() if isinstance(subject, URIRef) else subject
    for subject
    in g.subjects(None, None, True)
])

i = 0
while i < len(subjects):
    subject = subjects[i]
    source = subject[0].defrag()
    format = subject[1]

    # if source not in sources:
    #     # Add this source to the graph
    #     print(f'Adding {source=}')

    g.parse(source=source, format=format)

    # Determine if the new triples have an object which
    # we want to follow
    for object in g.objects(subject, None):
        if isinstance(object, URIRef):
            newsubject = object
            if newsubject not in subjects and any(newsubject.startswith(follow) for follow in follows):
                subjects.append(newsubject)

    i += 1


# Print out the combined Graph in the RDF Turtle format
#print(g.serialize(format="turtle"))
print(f'Triples at end: {len(g)}')

g.close()
