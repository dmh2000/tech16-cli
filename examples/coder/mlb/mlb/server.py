import http.server
import socketserver
import os

PORT = 8000
DIRECTORY = "."  # Serve files from the current directory

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

Handler = MyHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"serving at port {PORT}")
    print(f"serving files from directory: {os.path.abspath(DIRECTORY)}")
    print(f"try opening http://localhost:{PORT} in your browser")
    httpd.serve_forever()