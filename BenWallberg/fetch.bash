#!/bin/bash

# Get publicly available RDF from my Solid POD
#
# This curl command works, but the subject would be lost
# curl https://wallberg.solidcommunity.net/profile/card#me > solid.ttl
#
# Rapper can also retrieve via HTTP and knows how to preserve the subject

rapper -i turtle -o turtle https://wallberg.solidcommunity.net/profile/card#me > solid.ttl


# Fetch schema.org information from the Libraries' Staff Directory
# This loses the subject

any23 rover -e html-embedded-jsonld -f turtle -o staff-directory.ttl https://www.lib.umd.edu/directory/staff/wallberg


# Fetch ORCID public information
# ORCID does not currently distribute works information via RDF
#
rapper -o turtle https://orcid.org/0000-0002-4904-005X > orcid.ttl
