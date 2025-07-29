#!/bin/sh

# create two temporary files
MLB=$(mktemp)
trap 'rm -f "$MLB"' EXIT

# ------------------------------------
# scrape and process the mlb web page
# one-shot with example
# ------------------------------------
echo "<prompt>\
the input data is today's major league baseball games.\
-from that data create a file "mlb/mlb.csv" that contains: \
  -the visitor team abbreviation, \
  -the home team abbreviation, \
  -the current visitor score or 0 if not playing yet \
  -the current home team score or 0 if not playing yet \
  -an indicator of either: \
      -game time if not started \
      -current inning if in progress \
      -"final" if game is over \
\
Here is an example of the output file, not real data \
\
visitor,home,visitor_score,home_score,status \
TOR,BAL,0,0,6:35 PM ET \
COL,CLE,0,0,7 \
AZ,DET,0,0,final \
\
write the file to 'mlb/mlb.csv \
</prompt> \
\
do not output any description or examplation. output only the mlb/mlb.csv file. \
" >$MLB

# read the csv file (place the prompt last)
../../../src/tech16-coder/tech16-coder --model o4-mini https://mlb.com/schedule $MLB >mlb-csv.log

echo "done"