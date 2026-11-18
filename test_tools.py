from fastapi.testclient import TestClient
from app.main import app
from app.tools import create_ticket

client = TestClient(app)

def test_mock_order_found():
    assert client.get("/mock/orders/1001").json()["status"] == "shipped"

def test_mock_order_not_found():
    assert client.get("/mock/orders/9999").status_code == 404

def test_ticket_dry_run(monkeypatch):
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    assert create_ticket("teste", "low")["ticket"] == "DRY-RUN-001"
