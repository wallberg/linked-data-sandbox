#!/usr/bin/env python3

from rdflib import Dataset
from rdflib.term import URIRef

from config import Config

config = Config()

# Initial list of subjects to populate the graph
subjects = []
for graph in config.config["graphs"]:
    identifier = graph["identifier"]
    for source in graph["sources"]:
        subject = URIRef(source["iri"])
        format = source.get("format", None)
        subjects.append((identifier, subject, format))

# Set of subject base patterns we are willing to follow from
# discovered objects
follows = set(
    [
        # "https://fcrepo.lib.umd.edu/fcrepo/",
        URIRef("http://vocab.lib.umd.edu/"),
    ]
)

store_db = config.config["store_db"]

# Create or open a Graph with Berkeley DB persistence store
dbpath = store_db["file"]
ds = Dataset(store="BerkeleyDB")
ds.open(dbpath, create=True)

print(f"Triples at start: {len(ds)}")

# Document sources we have already fetched
sources = set(
    [
        subject.defrag() if isinstance(subject, URIRef) else subject
        for subject in ds.subjects(None, None, True)
    ]
)

i = 0
while i < len(subjects):
    subject = subjects[i]
    identifier = subject[0]
    source = subject[1].defrag()
    format = subject[2]

    if source not in sources:
        # Add this source to the graph
        print(f"Adding {identifier=}, {source=}")
        g = ds.graph(identifier)

        if format == "json-ld":
            g.parse(source=source, format=format, base=source)
        else:
            g.parse(source=source, format=format)

        # Determine if the new triples have an object which
        # we want to follow
        for object in ds.objects(subject, None):
            if isinstance(object, URIRef):
                newsubject = object
                if newsubject not in subjects and any(
                    newsubject.startswith(follow) for follow in follows
                ):
                    subjects.append((newsubject, None))

    i += 1

ds.close()
