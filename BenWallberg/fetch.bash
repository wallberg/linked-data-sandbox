#!/bin/bash

# Get publicly available RDF from my Solid POD
#
# This curl command works, but the subject would be lost
# curl https://wallberg.solidcommunity.net/profile/card#me > solid.ttl

python -m rdflib.tools.rdfpipe -i turtle -o turtle https://wallberg.solidcommunity.net/profile/card#me > solid.ttl

# Fetch ORCID public information

python -m rdflib.tools.rdfpipe -i turtle -o turtle https://orcid.org/0000-0002-4904-005X > orcid.ttl
python -m rdflib.tools.rdfpipe -i json-ld -o turtle https://orcid.org/0000-0002-4904-005X > orcid-works.ttl
