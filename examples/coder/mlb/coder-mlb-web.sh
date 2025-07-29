#!/bin/sh

# wipe the existing output in directory 'web'
rm -rf web

# create two temporary files
WEB=$(mktemp)
trap 'rm -f "$WEB"' EXIT

# ----------------------------
# construct the web app 
# ----------------------------
echo "- this web application will show the status of major league baseball MLB games \
- create a web page using html, css and js. \
- on startup and every 30 seconds the web app will fetch a copy of the mlb csv file from the API endpoint 'http://localhost:8001/mlb.csv. \
- the web app will fetch the mlb csv file using a GET request \
- the web app will parse the mlb csv file data and display the status of each game in a separate 'card'. \
- the web app should not use a Cache-Control header because it causes a CORS error \
- each card will show the teams, scores and status from the mlb.csv file \
- write html code to file 'mlb/index.html' \
- write css code to file 'mlb/index.css' \
- write javascript code to file 'mlb/index.js' \
- the web site should be professional and be targeted toward baseball fans \
- the web site should white background and colorful otherwise \
 - here is an example of the mlb.csv file \
visitor,home,visitor_score,home_score,status  \
TOR,BAL,0,0,6:35 PM ET  \
COL,CLE,0,0,6:40 PM ET  \
AZ,DET,0,0,6:40 PM ET \
" >$WEB 

# request claude sonnet to build the application
../../../src/tech16-coder/tech16-coder --model claude-sonnet-4-20250514 $WEB

# quit on error
if [ $? -ne 0 ]; then
    return $?
fi

# ----------------------------
# create the web server
# ----------------------------
SERVER=$(mktemp)
trap 'rm -f "$SERVER"' EXIT

echo "create a simple python web server in 'mlb/server.py'. \
  this web server will serve index.html by default. \
  use standard python libraries only.
  write only the specified files, do not add any \
  explanation or other text outside the requested files\
  " >$SERVER

# request gemini flash to create the server
../../../src/tech16-coder/tech16-coder --model gemini-2.5-flash $SERVER

