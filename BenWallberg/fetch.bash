#!/bin/bash

# Get publicly available RDF from my Solid POD
#
# This curl command works, but the subject would be lost
# curl https://wallberg.solidcommunity.net/profile/card#me > solid.ttl

python -m rdflib.tools.rdfpipe -i turtle -o turtle https://wallberg.solidcommunity.net/profile/card#me > solid.ttl


# Fetch schema.org information from the Libraries' Staff Directory
# This loses the subject
# The Libraries' Website staff directory entry no longer contains embedded json-ld
#any23 rover -e html-embedded-jsonld -f turtle -o staff-directory.ttl https://www.lib.umd.edu/directory/staff/wallberg

# Fetch ORCID public information

python -m rdflib.tools.rdfpipe -i turtle -o turtle https://orcid.org/0000-0002-4904-005X > orcid.ttl
python -m rdflib.tools.rdfpipe -i json-ld -o turtle https://orcid.org/0000-0002-4904-005X > orcid-works.ttl
