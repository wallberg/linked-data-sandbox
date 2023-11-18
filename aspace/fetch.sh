#!/bin/bash

# Fetch from ArchivesSpace

# Spiro Agnew Papers
#
# Includes internal references to:
#    schema:creator <https://archives.lib.umd.edu//agents/people/5256>
#    schema:holdingArchive <https://archives.lib.umd.edu//repositories/2>
#
# The information included for subject https://archives.lib.umd.edu//repositories/2 in the document
# https://archives.lib.umd.edu/repositories/2/resources/963 does not include everything returned in
# the document https://archives.lib.umd.edu/repositories/2/resources/963 .

any23 rover -e html-embedded-jsonld -f turtle https://archives.lib.umd.edu/repositories/2/resources/963 > agnew-papers.ttl
any23 rover -e html-embedded-jsonld -f turtle https://archives.lib.umd.edu/agents/people/5256 > agnew.ttl
any23 rover -e html-embedded-jsonld -f turtle https://archives.lib.umd.edu/repositories/2 > scua.ttl
