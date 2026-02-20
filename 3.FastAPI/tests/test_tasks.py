import pytest
from fastapi.testclient import TestClient

from app import app, get_storage, InMemoryStorage


@pytest.fixture()
def client():
    test_storage = InMemoryStorage()

    # replace dependency
    app.dependency_overrides[get_storage] = lambda: test_storage

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


def test_create_task_returns_201_and_id(client):
    r = client.post("/tasks", json={"name": "buy milk"})
    assert r.status_code == 201
    data = r.json()
    assert data["id"] == 1
    assert data["name"] == "buy milk"
    assert data["done"] == False


def test_get_missing_returns_404(client):
    r = client.get("/tasks/999")
    assert r.status_code == 404
    assert r.json()["detail"] == "Task not found"


def test_delete_removes_task(client):
    r1 = client.post("/tasks", json={"name": "Task1"})
    task_id = r1.json()["id"]

    r2 = client.delete(f"/tasks/{ task_id }")
    assert r2.status_code == 204
    assert r2.text == ""

    r3 = client.get(f"/tasks/{ task_id }")
    assert r3.status_code == 404

