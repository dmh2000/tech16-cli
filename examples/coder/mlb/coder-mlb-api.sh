#!/bin/sh

# create two temporary files
API=$(mktemp)
trap 'rm -f "$API"' EXIT

# ------------------------------------
# scrape and process the mlb web page
# one-shot with example
# ------------------------------------
echo "# Create a Python web server with CSV file serving capability: \
  - Implement a web server using Python's built-in http.server module \
  - Create a single API endpoint at http://localhost:8001/mlb.csv \
  - Write the server code to path 'mlb/api.py' \
  - The endpoint should: \
    - Serve the the existing mlb.csv file from the same directory (mlb/) when it exists \
    - Return HTTP 404 with appropriate error message when the file doesn't exist \
    - Set proper Content-Type header (text/csv) for successful responses \
  - Handle server startup on port 8001 with proper error handling \
  - Include basic logging for requests and errors \
  - The server must handle an OPTION request that specifies Access-Control-Allow-Origin for all clients.
  - output only the mlb/api.py file. do not output any other descriptions or explanations. just the code.\
" >$API

# read the csv file (place the prompt last)
../../../src/tech16-coder/tech16-coder --model gemini-2.5-pro $API

