import http.server
import socketserver

print("Starting webserver at http://localhost:8000")
PORT = 8000

# SimpleHTTPRequestHandler serves files from the current working directory.
# It automatically serves 'index.html' or 'index.htm' when a directory is requested.
Handler = http.server.SimpleHTTPRequestHandler

# Create a TCP server with the custom handler
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()
