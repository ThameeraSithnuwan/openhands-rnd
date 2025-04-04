from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_todo():
    response = client.post(
        "/todos/",
        json={"title": "Test todo", "description": "Test description"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test todo"
    assert data["description"] == "Test description"
    assert data["status"] == "pending"
    assert "id" in data

def test_list_todos():
    # Create a todo first
    create_response = client.post(
        "/todos/",
        json={"title": "List test todo"}
    )
    assert create_response.status_code == 200

    # Get list of todos
    response = client.get("/todos/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_todo():
    # Create a todo first
    create_response = client.post(
        "/todos/",
        json={"title": "Get test todo"}
    )
    todo_id = create_response.json()["id"]

    # Get the todo
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == todo_id
    assert data["title"] == "Get test todo"

def test_complete_todo():
    # Create a todo first
    create_response = client.post(
        "/todos/",
        json={"title": "Complete test todo"}
    )
    todo_id = create_response.json()["id"]

    # Complete the todo
    response = client.put(f"/todos/{todo_id}/complete")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"

def test_delete_todo():
    # Create a todo first
    create_response = client.post(
        "/todos/",
        json={"title": "Delete test todo"}
    )
    todo_id = create_response.json()["id"]

    # Delete the todo
    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 200

    # Verify it's deleted
    get_response = client.get(f"/todos/{todo_id}")
    assert get_response.status_code == 404
