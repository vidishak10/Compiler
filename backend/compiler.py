import sqlite3
from flask import Flask, request, jsonify, g
import os
from flask_cors import CORS
from FileManager import FileManager


class SQLCompiler:
    def __init__(self, db_path):
        self.db_path = db_path

    def get_db(self):
        """Create a new database connection for each request"""
        if 'db' not in g:
            g.db = sqlite3.connect(self.db_path, check_same_thread=False)
            g.db.row_factory = sqlite3.Row  # to access columns by name
        return g.db

    def execute_sql(self, sql):
        """Execute SQL statement"""
        db = self.get_db()
        try:
            cursor = db.cursor()
            cursor.execute(sql)
            db.commit()
            # Convert Row objects to dictionaries
            results = [dict(row) for row in cursor.fetchall()]
            return results, None
        except sqlite3.Error as e:
            return None, str(e)

    def close(self):
        """Close database connection at the end of request"""
        db = getattr(g, 'db', None)
        if db:
            db.close()



# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow all origins

# Initialize SQLCompiler
compiler = SQLCompiler("mydatabase.db")

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

        with open(filename, 'w') as f:
            f.write(sql_to_save)
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

        try:
            with open(filename, 'r') as f:
                sql_loaded = f.read()
            return jsonify({"sql": sql_loaded}), 200
        except FileNotFoundError:
            return jsonify({"error": f"File '{filename}' not found."}), 404
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
