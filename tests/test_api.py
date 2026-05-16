from fastapi.testclient import TestClient
from api.server import app


def test_health():
    c = TestClient(app)
    r = c.get('/health')
    assert r.status_code == 200


def test_simulate_and_metrics():
    c = TestClient(app)
    r = c.post('/simulate', params={'requests': 200, 'seed': 3})
    assert r.status_code == 200
    m = c.get('/metrics')
    assert m.status_code == 200
    assert len(m.json()) >= 1
