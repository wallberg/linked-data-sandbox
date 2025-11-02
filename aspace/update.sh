#!/bin/bash

FUSEKI=http://localhost:3030/ld/update

s-update --service=$FUSEKI --update=update.rq
