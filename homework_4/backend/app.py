import os
import pyodbc
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This allows all origins by default

# Read your full Azure SQL connection string from an env var
conn_str = os.getenv("SQL_CONN_STR")
if not conn_str:
    raise RuntimeError("Please set the SQL_CONN_STR environment variable.")

# Connect & ensure our table exists
conn = pyodbc.connect(conn_str, autocommit=True)
cursor = conn.cursor()
cursor.execute("""
  IF OBJECT_ID('dbo.books','U') IS NULL
    CREATE TABLE dbo.books (
      id INT IDENTITY PRIMARY KEY,
      title NVARCHAR(200),
      author NVARCHAR(200),
      description NVARCHAR(1000)
    )
""")

@app.route("/books", methods=["GET", "POST"])
def books():
    if request.method == "GET":
        rows = cursor.execute("SELECT id, title, author, description FROM dbo.books").fetchall()
        cols = [c[0] for c in cursor.description]
        return jsonify([dict(zip(cols, r)) for r in rows])

    # POST: expect JSON { title, author, description }
    data = request.get_json()
    cursor.execute(
      "INSERT INTO dbo.books (title,author,description) VALUES (?,?,?)",
      data["title"], data["author"], data["description"]
    )
    return jsonify({"status":"created"}), 201


@app.route("/ping")
def ping():
    return "Backend is alive!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
