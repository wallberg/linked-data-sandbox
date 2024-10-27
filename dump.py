#!/usr/bin/env python3

from rdflib import plugin, Dataset
from rdflib.term import URIRef
from rdflib.store import Store

from config import Config

config = Config()

store_db = config.config["store_db"]

# Create or open a Graph with Level DB persistence store
store = plugin.get("LevelDB", Store)(identifier=URIRef(store_db["identifier"]))

dbpath = store_db["file"]

ds = Dataset(store)
ds.open(dbpath, create=False)

print(ds.serialize(format="trig"))
