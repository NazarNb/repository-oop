import json
import sqlite3
import pytest
from app import app, export_tasks, get_db_connection, init_db


@pytest.fixture
def temp_environment(tmp_path):
    """Створює тимчасову базу даних SQLite та тимчасовий JSON-файл для кожного тесту."""
    db_path = tmp_path / "test_app.db"
    export_path = tmp_path / "test_tasks.json"

    app.config["TESTING"] = True
    app.config["DATABASE"] = str(db_path)
    app.config["EXPORT_FILE"] = str(export_path)

    init_db(str(db_path))

    yield {"db_path": str(db_path), "export_path": str(export_path)}


@pytest.fixture
def client(temp_environment):
    """Фікстура тестового HTTP-клієнта Flask."""
    with app.test_client() as client:
        yield client


# --- 1. ТЕСТУВАННЯ ФАЙЛІВ (JSON) ---


def test_export_empty_list(temp_environment):
    """⭐ Додатково: перевірка експорту порожнього списку завдань."""
    export_path = temp_environment["export_path"]
    db_path = temp_environment["db_path"]

    export_tasks(file_path=export_path, db_path=db_path)

    with open(export_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data == []


def test_corrupted_json_handling(tmp_path):
    """⭐ Додатково: перевірка обробки пошкодженого JSON-файла."""
    corrupted_file = tmp_path / "corrupted.json"
    corrupted_file.write_text("{ invalid json syntax: ", encoding="utf-8")

    with pytest.raises(json.JSONDecodeError):
        with open(corrupted_file, "r", encoding="utf-8") as f:
            json.load(f)


# --- 2. ТЕСТУВАННЯ БАЗИ ДАНИХ (SQLite) ---


def test_multiple_tasks_order(temp_environment):
    """⭐ Додатково: створення двох завдань та перевірка їх порядку в БД."""
    db_path = temp_environment["db_path"]
    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO tasks (title) VALUES (?)", ("Перше завдання",))
    cursor.execute("INSERT INTO tasks (title) VALUES (?)", ("Друге завдання",))
    conn.commit()

    cursor.execute("SELECT title FROM tasks ORDER BY id ASC")
    rows = cursor.fetchall()
    conn.close()

    assert len(rows) == 2
    assert rows[0]["title"] == "Перше завдання"
    assert rows[1]["title"] == "Друге завдання"


# --- 3. ТЕСТУВАННЯ ВЕБЗАСТОСУНКУ (Flask API) ---


def test_create_task_success(client, temp_environment):
    """Перевірка успішного створення завдання через POST-запит (201)."""
    response = client.post("/tasks", json={"title": "Вивчити pytest"})

    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == "Вивчити pytest"
    assert "id" in data

    # Перевірка фактичного запису в SQLite
    conn = get_db_connection(temp_environment["db_path"])
    cursor = conn.cursor()
    cursor.execute("SELECT title FROM tasks WHERE id = ?", (data["id"],))
    row = cursor.fetchone()
    conn.close()
    assert row is not None
    assert row["title"] == "Вивчити pytest"


def test_create_task_missing_title(client):
    """⭐ Додатково: POST-запит без поля title повертає помилку 400."""
    response = client.post("/tasks", json={})
    assert response.status_code == 400
    assert response.get_json() == {"error": "Title is required"}


def test_delete_task_success(client, temp_environment):
    """🔥 Додатково: DELETE /tasks/<id> видаляє запис із БД та оновлює JSON-файл."""
    db_path = temp_environment["db_path"]
    export_path = temp_environment["export_path"]

    # 1. Створюємо завдання
    res_create = client.post("/tasks", json={"title": "Завдання для видалення"})
    task_id = res_create.get_json()["id"]

    # 2. Виконуємо DELETE-запит
    res_delete = client.delete(f"/tasks/{task_id}")
    assert res_delete.status_code == 200

    # 3. Перевіряємо відсутність у SQLite
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    conn.close()
    assert row is None

    # 4. Перевіряємо відсутність у JSON-файлі експорту
    with open(export_path, "r", encoding="utf-8") as f:
        exported_data = json.load(f)
    assert not any(task["id"] == task_id for task in exported_data)