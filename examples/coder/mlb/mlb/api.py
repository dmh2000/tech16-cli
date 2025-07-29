import http.server
import socketserver
import os
import logging

# --- Configuration ---
PORT = 8001
CSV_FILENAME = "mlb.csv"
# The script is expected to be in 'mlb/api.py', so the CSV file
# should be in the same 'mlb/' directory.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE_PATH = os.path.join(SCRIPT_DIR, CSV_FILENAME)

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info(f"{CSV_FILE_PATH}")


class APRequestHandler(http.server.SimpleHTTPRequestHandler):
    """
    Custom request handler to serve a specific CSV file, handle CORS,
    and provide clear logging.
    """

    def do_OPTIONS(self):
        """Handle pre-flight CORS OPTIONS requests."""
        self.send_response(200)  # No Content
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        logging.info(f"Handled OPTIONS request from {self.client_address[0]}")

    def do_GET(self):
        """Handle GET requests."""
        if self.path == "/mlb.csv":
            self.handle_csv_request()
        else:
            self.send_error(404, "Not Found: Only /mlb.csv is a valid endpoint.")
            logging.warning(
                f"404 Not Found for path: {self.path} from {self.client_address[0]}"
            )

    def handle_csv_request(self):
        """
        Serve the mlb.csv file if it exists, otherwise return a 404 error.
        """
        if not os.path.exists(CSV_FILE_PATH):
            error_message = f"File not found: {CSV_FILENAME}"
            self.send_error(404, error_message)
            logging.error(f"Attempt to access non-existent file: {CSV_FILE_PATH}")
            return

        try:
            with open(CSV_FILE_PATH, "rb") as f:
                # Get file stats to set content-length and last-modified headers
                fs = os.fstat(f.fileno())

                self.send_response(200)
                self.send_header("Content-Type", "text/csv")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Content-Length", str(fs.st_size))
                self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
                self.end_headers()

                # Copy file content to the response
                self.copyfile(f, self.wfile)
                logging.info(
                    f"Successfully served {CSV_FILENAME} to {self.client_address[0]}"
                )

        except IOError as e:
            self.send_error(500, f"Server error reading file: {e}")
            logging.error(f"IOError while reading {CSV_FILE_PATH}: {e}")

    def log_message(self, format, *args):
        """Suppress the default SimpleHTTPRequestHandler logging."""
        # We use the 'logging' module for more structured logs.
        return


def run_server(
    server_class=socketserver.TCPServer, handler_class=APRequestHandler, port=PORT
):
    """
    Starts the HTTP server on the specified port with proper error handling.
    """
    try:
        with server_class(("", port), handler_class) as httpd:
            logging.info(f"Server starting on http://localhost:{port}")
            logging.info(f"Serving endpoint: /mlb.csv")
            logging.info(f"Expecting file at: {CSV_FILE_PATH}")
            httpd.serve_forever()
    except OSError as e:
        logging.error(
            f"Could not start server on port {port}: {e}. Port may be in use."
        )
    except KeyboardInterrupt:
        logging.info("Server shutting down gracefully.")
        # The 'with' statement ensures httpd.server_close() is called.


if __name__ == "__main__":
    run_server()
