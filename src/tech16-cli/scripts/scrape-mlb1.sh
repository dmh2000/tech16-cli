#!/bin/sh

# pipe std as prompt 
echo "\
read the specified url and extract the MLB game \
scores and upcoming games for today. print them out in a table" |
../src/tech16-cli/tech16-cli --model gemini-2.5-flash https://mlb.com


