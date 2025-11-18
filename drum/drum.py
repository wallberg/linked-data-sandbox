#!/usr/bin/env python3

from oaipmh.client import Client
from oaipmh.common import Metadata, Header
from oaipmh.metadata import MetadataRegistry

from lxml import etree

from pathlib import Path

from rdflib import Dataset, Namespace
from rdflib.namespace import RDF
from rdflib.term import URIRef, BNode

class ElementMetadataReader(object):
    """A "return the entire element" implementation of a reader.
    """

    def __call__(self, element):
        map = {}
        map['element'] = element
        return Metadata(element, map)

ENDPOINT = 'https://api.drum.lib.umd.edu/server/oai/request'

ds = Dataset()

g = ds.graph("https://drum.lib.umd.edu/")

registry = MetadataRegistry()
registry.registerReader('qdc', ElementMetadataReader())

client = Client(ENDPOINT, registry)
for n, record in enumerate(client.listRecords(metadataPrefix='qdc')):

    header: Header = record[0]
    metadata: Metadata = record[1]

    # print(f"Identifier: {header.identifier()}")
    # print(f"Datestamp: {header.datestamp()}")
    # print(f"Sets: {header.setSpec()}")

    if metadata is not None:
        if (element := metadata.getField('element')) is not None:
            # Get the qdc:qualifieddc element
            qdc = element.find("{http://dspace.org/qualifieddc/}qualifieddc")

            # Add an rdf:about attribute
            qdc.set("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about", header.identifier())

            qdc_bytes = etree.tostring(qdc,encoding='utf-8', method='xml')
            # print(qdc_string.decode('utf-8'))

            g.parse(source=qdc_bytes, format="xml")

    if n % 1000 == 0:
        print(f"--- Record {n} ---")

ds.serialize(destination=Path("./drum.trig"), format="trig")
