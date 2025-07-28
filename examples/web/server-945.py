import http.server
import socketserver
import os

PORT = 8000 # Port to serve on
HOST = "" # Empty string means serve on all available interfaces (e.g., localhost, network IP)

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    """
    A custom HTTP request handler that serves 'index.html' by default
    when the root path ('/') is requested.
    """
    
    def do_GET(self):
        # If the requested path is the root, rewrite it to 'index.html'.
        # This ensures that accessing http://localhost:8000/ will serve index.html.
        if self.path == '/':
            self.path = '/index.html'
        
        # Call the base class's do_GET method to handle the request.
        # This method automatically handles reading the file, setting
        # content type, and sending the response for the (possibly modified) path.
        super().do_GET()

if __name__ == "__main__":
    # Create a TCP server with the custom handler.
    # The server will listen on the specified HOST and PORT.
    # It will serve files from the directory where this script is executed.
    with socketserver.TCPServer((HOST, PORT), CustomHandler) as httpd:
        print(f"Serving HTTP on http://localhost:{PORT}/")
        print(f"Serving files from current directory: {os.getcwd()}")
        print("To stop the server, press Ctrl+C")
        
        try:
            # Activate the server; this will keep running until interrupted (e.g., by Ctrl+C).
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
            httpd.shutdown() # Cleanly shut down the server