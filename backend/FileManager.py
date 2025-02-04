import os
import sqlite3

class FileManager:
    @staticmethod
    def create_file(filename, content=""):
        """Create a new file with the provided content."""
        try:
            with open(filename, 'w') as f:
                f.write(content)
            return {"message": f"File '{filename}' created successfully."}, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def open_file(filename):
        """Open a file and read its content."""
        try:
            with open(filename, 'r') as f:
                content = f.read()
            return content, None
        except FileNotFoundError:
            return None, f"File '{filename}' not found."
        except Exception as e:
            return None, str(e)

    @staticmethod
    def view_file(filename):
        """View the content of a file."""
        try:
            with open(filename, 'r') as f:
                content = f.read()
            return content, None
        except FileNotFoundError:
            return None, f"File '{filename}' not found."
        except Exception as e:
            return None, str(e)

    @staticmethod
    def insert_into_file(filename, content):
        """Insert content into an existing file."""
        try:
            with open(filename, 'a') as f:
                f.write(content)
            return {"message": f"Content added to '{filename}' successfully."}, None
        except FileNotFoundError:
            return None, f"File '{filename}' not found."
        except Exception as e:
            return None, str(e)

    @staticmethod
    def delete_file(filename):
        """Delete a file."""
        try:
            if os.path.exists(filename):
                os.remove(filename)
                return {"message": f"File '{filename}' deleted successfully."}, None
            else:
                return None, f"File '{filename}' not found."
        except Exception as e:
            return None, str(e)

    @staticmethod
    def save_sql_in_db(db_filename, sql_code):
        """Save SQL code into the database."""
        try:
            # Establish a connection to the database
            connection = sqlite3.connect(db_filename)
            cursor = connection.cursor()

            # Create a table to store SQL code if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sql_queries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sql_code TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # Insert the SQL code into the table
            cursor.execute("INSERT INTO sql_queries (sql_code) VALUES (?);", (sql_code,))
            connection.commit()

            connection.close()
            return {"message": "SQL code saved to the database successfully."}, None
        except Exception as e:
            return None, str(e)
