# Vanguard Drink Bot
This includes the pi GPIO controller, api/server, and UI.
## Installation
TODO
## Starting the Server
run `python server.py`
Note that this requires Python 3.5+
## Shutting Down the Server Cleanly
Send a POST request to the `/shutdown` endpoint. This will properly clean up GPIO pins before stopping the Flask server.
