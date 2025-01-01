#!/usr/bin/env python3

import os
import sys

from pathlib import Path

from pprint import pprint

from rdflib import Dataset, Namespace, XSD
from rdflib.namespace import RDF
from rdflib.term import URIRef, BNode, Literal

from asnake.aspace import ASpace
import asnake.logging as logging

from dotenv import load_dotenv

import requests
import xmltodict

# Add any environment variables from .env
load_dotenv('../.env')

# Get environment variables
env = {}
for key in ('ASPACE_API_URL', 'ASPACE_API_USERNAME',
            'ASPACE_API_PASSWORD', 'ASPACE_PUBLIC_URL'):
    env[key] = os.environ.get(key)
    if env[key] is None:
        raise RuntimeError(f'Must provide environment variable: {key}')

debug=False

SCHEMA = Namespace("http://schema.org/")
ASPACE = Namespace("https://archives.lib.umd.edu/")

ds = Dataset()
ds.bind("schema", SCHEMA)
ds.bind("aspace", ASPACE)

g = ds.graph(ASPACE)

# Setup the ArchivesSnake library
config = {
    'baseurl': env['ASPACE_API_URL'],
    'username': env['ASPACE_API_USERNAME'],
    'password': env['ASPACE_API_PASSWORD'],
    'default_config': 'INFO_TO_STDERR',
}

logger = logging.get_logger("sitemap")
if debug:
    logging.setup_logging(stream=sys.stderr, level="DEBUG")
else:
    logging.setup_logging(stream=sys.stderr, level="INFO")

logger.debug(f'config={config}')

logger.info("Begin generating sitemap.xml")

aspace = ASpace(**config)

# Authorize as the provided username
aspace.authorize()

# Iterate over published repositories
# for repo in [aspace.repositories(2)]:
for repo in aspace.repositories:
    if repo.publish:

        repo_uri = URIRef(ASPACE + repo.uri)

        # Iterate over published digital objects
        # for do in [repo.digital_objects(10000)]:
        for do in repo.digital_objects:
            if do.publish:

                object_uri = URIRef(ASPACE + do.uri)

                logger.info(f"{object_uri=}")

                if debug:
                    pprint(vars(do))

                g.add((object_uri, RDF.type, URIRef(SCHEMA + "ArchiveComponent")))
                g.add((object_uri, RDF.type, URIRef(SCHEMA + "MediaObject")))

                g.add((object_uri, URIRef(SCHEMA + "holdingArchive"), repo_uri))
                g.add((object_uri, URIRef(SCHEMA + "name"), Literal(do.title)))
                g.add((object_uri, URIRef(SCHEMA + "dateCreated"),
                    Literal(do.create_time, datatype=XSD.dateTime)))

                for collection in do.collection:
                    g.add((object_uri, URIRef(SCHEMA + "isPartOf"), URIRef(ASPACE + collection.ref)))

                # Get most recent file_version
                file_versions = list(do.file_versions)
                if len(file_versions) > 0:
                    file_version = file_versions[0]
                    g.add((object_uri, URIRef(SCHEMA + "dateModified"),
                        Literal(file_version.user_mtime, datatype=XSD.dateTime)))

                    uris = []
                    if "file_uri" in dir(file_version):
                        uris.append(file_version.file_uri)
                    if "link_uri" in dir(file_version):
                        uris.append(file_version.link_uri)

                    for uri in uris:
                        if "iiif.lib.umd.edu" in uri:
                            g.add((object_uri, URIRef(SCHEMA + "thumbnailUrl"), Literal(uri)))
                        else:
                            if "hdl.handle.net" in uri:
                                g.add((object_uri, URIRef(SCHEMA + "sameAs"), Literal(uri)))
                            g.add((object_uri, URIRef(SCHEMA + "url"), Literal(uri)))

                # creator?

# print(ds.serialize(format="trig"))
ds.serialize(destination=Path("./aspace-objects.trig"), format="trig")
