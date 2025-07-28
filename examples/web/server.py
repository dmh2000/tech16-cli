import http.server
import socketserver
import os

PORT = 8000
DIRECTORY = "." # Serve files from the current directory

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Set the directory for the handler to serve files from
        super().__init__(*args, directory=DIRECTORY, **kwargs)

# Create a TCP server with the custom handler
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Serving HTTP on port {PORT} from directory: {os.path.abspath(DIRECTORY)}")
    print("To access, open your browser and go to http://localhost:8000/")
    print("Press Ctrl+C to stop the server.")
    # Activate the server; this will keep running until interrupted
    httpd.serve_forever()