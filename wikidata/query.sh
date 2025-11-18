#!/bin/bash

FUSEKI=http://localhost:3030/ld/query

s-query --service=$FUSEKI --query=query.rq
