#!/usr/bin/env python3

from os import path

from rdflib import plugin, Dataset
from rdflib.term import URIRef
from rdflib.store import Store

from config import Config

config = Config()

# Initial list of subjects to populate the graph
subjects = []
for graph in config.config["graphs"]:
    for source in graph["sources"]:
        subject = URIRef(source["iri"])
        format = source.get("format", None)
        subjects.append((subject, format))

# Set of subject base patterns we are willing to follow from
# discovered objects
follows = set([
    # "https://fcrepo.lib.umd.edu/fcrepo/",
    URIRef("http://vocab.lib.umd.edu/"),
])

store_db = config.config["store_db"]

# Create or open a Graph with Level DB persistence store
store = plugin.get("LevelDB", Store)(identifier=URIRef(store_db["identifier"]))

dbpath = store_db["file"]
create = not path.exists(dbpath)

ds = Dataset(store)
ds.open(dbpath, create=create)

print(f'Triples at start: {len(ds)}')

# Document sources we have already fetched
sources = set([
    subject.defrag() if isinstance(subject, URIRef) else subject
    for subject
    in ds.subjects(None, None, True)
])

i = 0
while i < len(subjects):
    subject = subjects[i]
    source = subject[0].defrag()
    format = subject[1]

    if source not in sources:
        # Add this source to the graph
        print(f'Adding {source=}')

        ds.parse(source=source, format=format)

        # Determine if the new triples have an object which
        # we want to follow
        for object in ds.objects(subject, None):
            if isinstance(object, URIRef):
                newsubject = object
                if newsubject not in subjects and any(newsubject.startswith(follow) for follow in follows):
                    subjects.append((newsubject, None))

    i += 1


# Print out the combined Graph in the RDF Turtle format
#print(g.serialize(format="turtle"))
print(f'Triples at end: {len(ds)}')

ds.close()
