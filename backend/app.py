
# @app.route('/<path:filename>')
# def serve_static(filename):
#     return send_from_directory('static', filename)

# @socketio.on('connect')
# def handle_connect():
#     print("Client connected")

# if __name__ == "__main__":
#     socketio.run(app, debug=True)

#----------------------Main Working Code-------------------------------------------------------------------#

from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import mysql.connector
import psycopg2
import logging
from config import DATABASES  # Ensure config.py exists and is correctly configured

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Database connectors
def get_db_connection(db_type):
    try:
        if db_type == "sqlite":
            conn = sqlite3.connect("database.db")
        elif db_type == "mysql":
            conn = mysql.connector.connect(**DATABASES["mysql"])
        elif db_type == "postgresql":
            conn = psycopg2.connect(**DATABASES["postgresql"])
        else:
            raise ValueError(f"Unsupported database type: {db_type}")
        return conn
    except Exception as e:
        logging.error(f"Database connection error: {str(e)}")
        return None

@app.route("/")
def home():
    return "Flask server is running!"

# Test database connection
@app.route("/test-db/<db_type>")
def test_db(db_type):
    try:
        conn = get_db_connection(db_type)
        if conn:
            conn.close()
            return jsonify({"message": f"Connected to {db_type} successfully!"})
        else:
            return jsonify({"error": f"Failed to connect to {db_type}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/execute', methods=['POST'])
def execute_sql():
    try:
        data = request.json
        query = data.get('sql', '').strip()
        db_type = data.get('db_type', 'sqlite')

        logging.debug(f"Received query: {query} | DB Type: {db_type}")

        if not query:
            return jsonify({"error": "No SQL query provided"}), 400

        conn = get_db_connection(db_type)
        if not conn:
            return jsonify({"error": f"Failed to connect to {db_type} database"}), 500

        cursor = conn.cursor()

        # Prevent multiple queries execution
        if ";" in query and db_type in ["mysql", "postgresql"]:
            return jsonify({"error": "Multiple queries in a single request are not allowed"}), 400

        cursor.execute(query)

        if query.lower().startswith("select"):
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description] if cursor.description else []
            conn.close()
            return jsonify({"isSelect": True, "result": [dict(zip(columns, row)) for row in result]})

        conn.commit()
        conn.close()
        return jsonify({"isSelect": False, "result": "Query executed successfully!"})

    except sqlite3.Error as e:
        logging.error(f"SQLite error: {str(e)}")
        return jsonify({"error": f"SQLite error: {str(e)}"}), 500
    except mysql.connector.Error as e:
        logging.error(f"MySQL error: {str(e)}")
        return jsonify({"error": f"MySQL error: {str(e)}"}), 500
    except psycopg2.Error as e:
        logging.error(f"PostgreSQL error: {str(e)}")
        return jsonify({"error": f"PostgreSQL error: {str(e)}"}), 500
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
