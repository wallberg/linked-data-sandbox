#!/bin/bash

# Fetch from ArchivesSpace

# Spiro Agnew Papers
#

rdfpipe -i json-ld -o turtle https://archives.lib.umd.edu/repositories/2/resources/963 > agnew-papers.ttl

# Includes internal references to:
#  Spiro Agnew:  schema:creator <https://archives.lib.umd.edu//agents/people/5256>
#  SCUA:         schema:holdingArchive <https://archives.lib.umd.edu//repositories/2>
#
# The information included for subject https://archives.lib.umd.edu/repositories/2/resources/963 is a subset of
# what is included when you request the document https://archives.lib.umd.edu/repositories/2/resources/963 .

# It appears that digital objects don't contain JSON-LD, eg https://archives.lib.umd.edu/repositories/2/digital_objects/16835

rdfpipe -i json-ld -o turtle https://archives.lib.umd.edu/agents/people/5256 > agnew.ttl
rdfpipe -i json-ld -o turtle https://archives.lib.umd.edu/repositories/2 > scua.ttl
