#!/bin/sh

# create two temporary files
API=$(mktemp)
trap 'rm -f $API"' EXIT

# ------------------------------------
# scrape and process the mlb web page
# one-shot with example
# ------------------------------------
echo "- create a web server with one API endpoint 'http://localhost:8001/mlb.csv' \
- use the Python programming language \
- use the standard Python http functions \
- use a single file, 'mlb/api.py' for the application \
- the endpoint returns a copy of the file 'mlb.csv' or a 404 error \
" >$API

# read the csv file (place the prompt last)
../../../src/tech16-coder/tech16-coder --model gemini-2.5-flash $API

echo "done"