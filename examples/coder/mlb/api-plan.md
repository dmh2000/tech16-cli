The following is a description I want to create using gemini 2.5 pro. Can you
improvie this prompt

<prompt>
- create a web server with one API endpoint 'http://localhost:8001/mlb.csv'
- implement the server using the Python programming language
- use the standard Python http functions
- write the server python file to 'mlb/api.py'
- assume there will be a file 'mlb.csv' in the same directory as the server
- the endpoint returns a copy and existing 'mlb.csv' file in the same directory
  as the server, or a 404 error if the file doesnt exist
<prompt>

1.  **Objective Clarification**:

    - **Purpose**: To create a minimal, self-contained HTTP server capable of serving a static CSV file. This server will act as a local data source for development and testing purposes, mimicking a simple data API.
    - **Scope**: A single API endpoint to serve a specific local file. No complex routing, database integration, or dynamic content generation is required.

2.  **Stakeholder Mapping**:

    - **Primary User**: A local developer/data scientist who needs to access `mlb.csv` via HTTP.
    - **Developer (You/AI)**: Responsible for delivering the code and setup instructions.

3.  **Constraint Assessment**:

    - **Technology**: Python 3.x.
    - **Libraries**: Must exclusively use standard Python `http` module functions (e.g., `http.server`). No external frameworks (like Flask, Django, FastAPI) are permitted to keep the footprint minimal.
    - **Endpoint**: `http://localhost:8001/mlb.csv`.
    - **File Location**: The `mlb.csv` file is expected to reside in the same directory as the server script.

4.  **Success Criteria**:

    - The server starts successfully and listens on the specified port.
    - A GET request to `http://localhost:8001/mlb.csv` successfully returns the content of the `mlb.csv` file when it exists.
    - A GET request to `http://localhost:8001/mlb.csv` returns a 404 Not Found HTTP status code if `mlb.csv` does not exist in the expected location.
    - The generated code is clean, readable, well-commented, and adheres to standard Python best practices for simplicity.

5.  **Environmental Factors**:
    - Assumes a standard local development environment with Python installed.
    - The `mlb.csv` file will be pre-existing and managed separately.
