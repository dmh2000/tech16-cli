## prompt for MLB csv file

scrape https://mlb.com/schedule and get todays baseball games.
from the input data create a file "mlb/mlb.csv" that contains
the visitor team abbreviation,
the home team abbreviation,
the current visitor score or 0 if not playing yet
the current home team score or 0 if not playing yet
an indicator of either:

- game time if not started
- current inning if in progress
- "final" if game is over

Here is an example

```mlb.csv
tor,bal,0,0,6:36
col,cle,1,2,7
az,det,2,1,final
```

## API endpoint

- create a web server with one API endpoint 'http://localhost:8001/mlb.csv'
- use the Python programming language
- use the standard Python http functions
- write the server python file to 'mlb/api.py'
- a separate application will cretae a file in the mlb directory named mlb.csv
- the endpoint returns a copy and existing 'mlb.csv' file in the same directory as the server, or a 404 error if the file doesnt exist

## Web Page

- this web application will show the status of major league baseball MLB games
- create a web page using html, css and js.
- on startup and every 30 seconds the web app will fetch a copy of the mlb csv file from the API endpoint 'http://localhost:8001/mlb.csv.
- the web app will parse the mlb csv file data and display the status of each game in a separate 'card'.
- each card will show the teams, scores and status from the mlb.csv file
- write html code to file "mlb/index.html"
- write css code to file "mlb/index.css"
- write javascript code to file "mlb/index.js
- the web site should be professional and be targeted toward baseball fans
- the web site should white background and colorful otherwise

- here is an example of the mlb.csv file

visitor,home,visitor_score,home_score,status
TOR,BAL,0,0,6:35 PM ET
COL,CLE,0,0,6:40 PM ET
AZ,DET,0,0,6:40 PM ET

## Server
