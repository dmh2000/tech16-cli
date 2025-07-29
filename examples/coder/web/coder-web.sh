#!/bin/sh

# wipe the existing output in directory 'web'
rm -rf web

# create two temporary files
WEB=$(mktemp)
trap 'rm -f "$WEB"' EXIT

# ----------------------------
# construct the web app 
# ----------------------------
echo "make the web page modern and colorful \
  it should have link to sqirvy.xyz \
  create 3 files in directory 'web' \
  write html code go file 'web/index.html' \
  write css code to file 'web/index.css' \
  write javascript code to file 'web/index.js' \
  write only the specified files, do not add any \
  explanation or other text outside the requested files\
  " >$WEB

# request claude sonnet to build the application
../../../src/tech16-coder/tech16-coder --model claude-sonnet-4-20250514 $WEB

# quit on error
if [ $? -ne 0 ]; then
    rm $WEB
    return $?
fi
rm $WEB 2>/dev/null   

# ----------------------------
# create the web server
# ----------------------------
SERVER=$(mktemp)
trap 'rm -f "$SERVER"' EXIT
echo "create a simple python web server in 'web/server.py'. \
  this web server will serve index.html by default. \
  use standard python libraries only.
  write only the specified files, do not add any \
  explanation or other text outside the requested files\
  " >$SERVER

# request gemini flash to create the server
../../../src/tech16-coder/tech16-coder --model gemini-2.5-flash $SERVER

# quit on error
if [ $? -ne 0 ]; then
    rm $SERVER
    return $?
fi
rm $SERVER 2>/dev/null

echo "start the web server"
cd web && python web/server.py 