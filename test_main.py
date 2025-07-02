from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZ2hhIiwiaWQiOjgsImV4cCI6MTc1MTQwNDY3M30.PZdE4vv_TtS9lKoGYliUMSnHdWo4BnuFgE5q-N1CXQ4"

def test_post_completed():
    headers = {"Authorization": f"Bearer {token}"}
    task_id = 19

    response = client.post(f"/tasks/{task_id}/complete", headers = headers)

    assert response.status_code == 200
    json_response = response.json()
    assert json_response["id"] == task_id
    assert json_response["status"] == "Completed"


def test_filter_tasks():
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/tasks-by-status", headers = headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_tasks():
    headers = {"Authorization": f"Bearer {token}"}
    updated_data = {
        "title": "Updated Task",
        "description": "Updated description",
        "status": "In Progress",
        "user_id": "1"
    }
    create_response = client.post("/tasks", json=updated_data, headers=headers)
    assert create_response.status_code == 200
    task_id = create_response.json()["id"]

    response = client.put(f"/tasks/{task_id}", json=updated_data, headers=headers)
    assert response.status_code == 200

def test_delete_tasks():
    headers = {"Authorization": f"Bearer {token}"}

    task_data = {
        "title": "Task to delete",
        "description": "Temp task",
        "status": "New",
        "user_id": 1
    }
    create_response = client.post("/tasks", json=task_data, headers=headers)
    assert create_response.status_code == 200
    task_id = create_response.json()["id"]

    response = client.delete(f"/tasks/{task_id}", headers=headers)
    assert response.status_code == 200

def test_create_task():
    headers = {"Authorization": f"Bearer {token}"}

    task_data = {
        "title": "Test Task",
        "description": "Test description",
        "status": "New",       
        "user_id": 2      
    }

    response = client.post("/tasks", json = task_data, headers=headers)

    assert response.status_code == 200
    json_response = response.json()
    
    assert json_response["title"] == task_data["title"]
    assert json_response["description"] == task_data["description"]
    assert json_response["status"] == task_data["status"]
    assert json_response["user_id"] == task_data["user_id"]

def test_get_specific_task():
    headers = {"Authorization": f"Bearer {token}"}
    task_id = 14
    response = client.get(f"/tasks/{task_id}", headers = headers)
    assert response.status_code == 200

def test_get_user_tasks():
    headers = {"Authorization": f"Bearer {token}"}

    user_id = 1
    response = client.get(f"/tasks/user/{user_id}", headers = headers)
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_get_all_tasks():
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/tasks", headers = headers)
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


