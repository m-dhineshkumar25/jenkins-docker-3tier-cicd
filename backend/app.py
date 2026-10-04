from flask import Flask, jsonify
import os
import psycopg2

app = Flask(__name__)

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "postgres"),
        database=os.getenv("POSTGRES_DB", "cloudops"),
        user=os.getenv("POSTGRES_USER", "cloudops"),
        password=os.getenv("POSTGRES_PASSWORD", "cloudops123")
    )

@app.route("/api/health")
def health():
    try:
        conn = get_connection()
        conn.close()
        return jsonify({"status": "healthy", "service": "backend", "database": "connected"})
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

@app.route("/api/projects")
def projects():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, description FROM projects ORDER BY id")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify([
        {"id": r[0], "name": r[1], "description": r[2]}
        for r in rows
    ])

@app.route("/")
def home():
    return "CloudOps Backend API"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
