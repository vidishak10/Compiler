# from flask import Flask, request, jsonify
# import os
# from compiler import SQLCompiler, FileManager
# from compiler import SQLCompiler
# from FileManager import FileManager

# # Use FileManager for file operations where necessary


# # Initialize the Flask app
# app = Flask(__name__)

# # Initialize the database compiler and file manager
# try:
#     compiler = SQLCompiler("mydatabase.db")
#     file_manager = FileManager()
# except Exception as e:
#     print(f"Error initializing SQLCompiler or FileManager: {e}")
#     raise

# # Enable CORS for all origins
# from flask_cors import CORS
# CORS(app)  # This will allow all origins by default

# # Handle OPTIONS preflight requests (this may be redundant with CORS(app) enabled)
# @app.before_request
# def handle_options():
#     if request.method == "OPTIONS":
#         response = jsonify({"message": "CORS preflight response"})
#         response.headers["Access-Control-Allow-Origin"] = "*"
#         response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
#         response.headers["Access-Control-Allow-Headers"] = "Content-Type"
#         return response

# @app.route('/api/execute', methods=['POST'])
# def execute_sql():
#     """Endpoint to execute SQL code."""
#     try:
#         sql_code = request.get_json().get("sql")
#         if not sql_code:
#             return jsonify({"error": "SQL code is required."}), 400

#         results, error = compiler.execute_sql(sql_code)
#         if error:
#             return jsonify({"error": error}), 400
#         return jsonify({"results": results}), 200
#     except Exception as e:
#         return jsonify({"error": f"Unexpected error: {e}"}), 500

# @app.route('/api/save', methods=['POST'])
# def save_sql():
#     """Endpoint to save SQL code to a file."""
#     try:
#         data = request.get_json()
#         filename = data.get("filename")
#         sql_to_save = data.get("sql")

#         if not filename or not sql_to_save:
#             return jsonify({"error": "Filename and SQL code are required."}), 400

#         success, error = file_manager.save_sql(filename, sql_to_save)
#         if error:
#             return jsonify({"error": error}), 400
#         return jsonify({"message": f"File '{filename}' saved successfully."}), 200
#     except Exception as e:
#         return jsonify({"error": f"Unexpected error: {e}"}), 500

# @app.route('/api/load', methods=['POST'])
# def load_sql():
#     """Endpoint to load SQL code from a file."""
#     try:
#         data = request.get_json()
#         filename = data.get("filename")

#         if not filename:
#             return jsonify({"error": "Filename is required."}), 400

#         sql_loaded, error = file_manager.load_sql(filename)
#         if error:
#             return jsonify({"error": error}), 400
#         return jsonify({"sql": sql_loaded}), 200
#     except Exception as e:
#         return jsonify({"error": f"Unexpected error: {e}"}), 500

# @app.route('/', methods=['GET'])
# def home():
#     """Test endpoint to check server status."""
#     return jsonify({"message": "Server is running!"}), 200

# @app.teardown_appcontext
# def close_db(error):
#     """Close the database connection when the app context is torn down."""
#     try:
#         compiler.close()
#     except Exception as e:
#         print(f"Error closing database: {e}")

# def initialize_database():
#     """Initialize the database with the necessary schema."""
#     schema = """
#     CREATE TABLE IF NOT EXISTS example_table (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT NOT NULL,
#         description TEXT
#     );
#     """
#     try:
#         compiler.execute_sql(schema)
#         print("Database schema initialized.")
#     except Exception as e:
#         print(f"Error initializing database schema: {e}")

# if __name__ == '__main__':
#     # Ensure the database file exists and initialize the schema
#     if not os.path.exists("mydatabase.db"):
#         with open("mydatabase.db", "w") as f:
#             pass  # Create an empty file

#     initialize_database()

#     # Run the Flask application
#     app.run(debug=True, host="0.0.0.0", port=5000)


from flask import Flask, request, jsonify
import os
from compiler import SQLCompiler, FileManager
from flask_cors import CORS

# Initialize the Flask app
app = Flask(__name__)

# Initialize the database compiler and file manager
try:
    compiler = SQLCompiler("mydatabase.db")
    file_manager = FileManager()  # Assuming FileManager is implemented correctly
except Exception as e:
    print(f"Error initializing SQLCompiler or FileManager: {e}")
    raise

# Enable CORS for all origins
CORS(app)  # This will allow all origins by default

# Handle OPTIONS preflight requests (this may be redundant with CORS(app) enabled)
@app.before_request
def handle_options():
    if request.method == "OPTIONS":
        response = jsonify({"message": "CORS preflight response"})
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response

@app.route('/api/execute', methods=['POST'])
def execute_sql():
    """Endpoint to execute SQL code."""
    try:
        sql_code = request.get_json().get("sql")
        if not sql_code:
            return jsonify({"error": "SQL code is required."}), 400

        results, error = compiler.execute_sql(sql_code)
        if error:
            return jsonify({"error": error}), 400
        return jsonify({"results": results}), 200
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {e}"}), 500

@app.route('/api/save', methods=['POST'])
def save_sql():
    """Endpoint to save SQL code to a file."""
    try:
        data = request.get_json()
        filename = data.get("filename")
        sql_to_save = data.get("sql")

        if not filename or not sql_to_save:
            return jsonify({"error": "Filename and SQL code are required."}), 400

        success, error = file_manager.save_sql(filename, sql_to_save)
        if error:
            return jsonify({"error": error}), 400
        return jsonify({"message": f"File '{filename}' saved successfully."}), 200
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {e}"}), 500

@app.route('/api/load', methods=['POST'])
def load_sql():
    """Endpoint to load SQL code from a file."""
    try:
        data = request.get_json()
        filename = data.get("filename")

        if not filename:
            return jsonify({"error": "Filename is required."}), 400

        sql_loaded, error = file_manager.load_sql(filename)
        if error:
            return jsonify({"error": error}), 400
        return jsonify({"sql": sql_loaded}), 200
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {e}"}), 500

@app.route('/', methods=['GET'])
def home():
    """Test endpoint to check server status."""
    return jsonify({"message": "Server is running!"}), 200

@app.teardown_appcontext
def close_db(error):
    """Close the database connection when the app context is torn down."""
    try:
        compiler.close()
    except Exception as e:
        print(f"Error closing database: {e}")

def initialize_database():
    """Initialize the database with the necessary schema."""
    schema = """
    CREATE TABLE IF NOT EXISTS example_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT
    );
    """
    try:
        compiler.execute_sql(schema)
        print("Database schema initialized.")
    except Exception as e:
        print(f"Error initializing database schema: {e}")

if __name__ == '__main__':
    # Ensure the database file exists and initialize the schema
    if not os.path.exists("mydatabase.db"):
        with open("mydatabase.db", "w") as f:
            pass  # Create an empty file

    initialize_database()

    # Run the Flask application
    app.run(debug=True, host="0.0.0.0", port=5000)
