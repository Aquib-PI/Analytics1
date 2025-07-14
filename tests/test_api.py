# tests/test_api.py
import os, sys, pytest
from fastapi.testclient import TestClient

# 1) Make sure "backend" folder is on PYTHONPATH, so you can import main
root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, root)
sys.path.insert(0, os.path.join(root, "backend"))

# 2) import app
from backend.main import app

# 3) import the modules under the same name main.py used:
import API.api_dashboard      as api_dashboard # type: ignore
import API.financial_analysis_service as financial_api # type: ignore
import API.operational_ef    as operational_api # type: ignore
import API.demographic       as demographic_api # type: ignore
import API.risk_and_fraud_management as risk_api # type: ignore
import API.customer_insight  as customer_api # type: ignore

@pytest.fixture(autouse=True)
def mock_all_kpis(monkeypatch):
    dummy = lambda *args, **kwargs: {"metrics": [], "charts": []}

    # patch the modules FastAPI actually has wired up:
    monkeypatch.setattr(api_dashboard,      "fetch_dashboard_data",           dummy)
    monkeypatch.setattr(financial_api,      "get_financial_performance_data",  dummy)
    monkeypatch.setattr(operational_api,    "get_operational_efficiency_data", dummy)
    monkeypatch.setattr(demographic_api,    "get_demo_kpi_data",               dummy)
    monkeypatch.setattr(risk_api,           "get_risk_and_fraud_data",         dummy)
    monkeypatch.setattr(customer_api,       "get_customer_insights_data",      dummy)

@pytest.fixture
def client():
    return TestClient(app)

def test_dashboard(client):
    r = client.get("/api/dashboard")
    assert r.status_code == 200
    assert r.json() == {"metrics": [], "charts": []}

def test_financial_performance(client):
    resp = client.get("/api/financial-performance")
    assert resp.status_code == 200
    assert resp.json() == {"metrics": [], "charts": []}


def test_operational_efficiency(client):
    resp = client.get("/api/operational-efficiency")
    assert resp.status_code == 200
    assert resp.json() == {"metrics": [], "charts": []}


def test_demographic(client):
    resp = client.get("/api/demographic")
    assert resp.status_code == 200
    assert resp.json() == {"metrics": [], "charts": []}


def test_risk_and_fraud(client):
    resp = client.get("/api/risk-and-fraud")
    assert resp.status_code == 200
    assert resp.json() == {"metrics": [], "charts": []}


def test_customer_insights(client):
    resp = client.get("/api/customer-insights")
    assert resp.status_code == 200
    assert resp.json() == {"metrics": [], "charts": []}
