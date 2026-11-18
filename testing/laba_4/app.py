import json
import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)
DB_NAME = "app.db"
EXPORT_FILE = "tasks_export.json"


def get_db_connection(db_path=None):
    path = db_path or app.config.get("DATABASE", DB_NAME)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path=None):
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL
        )
    """
    )
    conn.commit()
    conn.close()


def export_tasks(file_path=None, db_path=None):
    path = file_path or app.config.get("EXPORT_FILE", EXPORT_FILE)
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM tasks ORDER BY id ASC")
    rows = cursor.fetchall()
    conn.close()

    tasks = [{"id": row["id"], "title": row["title"]} for row in rows]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


@app.route("/tasks", methods=["GET"])
def get_tasks():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM tasks ORDER BY id ASC")
    rows = cursor.fetchall()
    conn.close()
    tasks = [{"id": row["id"], "title": row["title"]} for row in rows]
    return jsonify(tasks), 200


@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    if not data or "title" not in data or not str(data["title"]).strip():
        return jsonify({"error": "Title is required"}), 400

    title = data["title"]
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()

    export_tasks()
    return jsonify({"id": task_id, "title": title}), 201


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()

    if not task:
        conn.close()
        return jsonify({"error": "Task not found"}), 404

    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

    export_tasks()
    return jsonify({"message": f"Task {task_id} deleted successfully"}), 200


if __name__ == "__main__":
    init_db()
    app.run(debug=True)