import os
import sys
from fastapi.testclient import TestClient

# Ensure backend modules can be imported
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Provide dummy DB connection details so modules import without error
os.environ.setdefault('DB_USER', 'user')
os.environ.setdefault('DB_PASSWORD', 'pass')
os.environ.setdefault('DB_HOST', 'localhost')
os.environ.setdefault('DB_PORT', '5432')
os.environ.setdefault('DB_NAME', 'test')

import main
import API.api_dashboard as api_dashboard
import API.financial_analysis_service as financial_api
import API.operational_ef as operational_api
import API.demographic as demographic_api
import API.risk_and_fraud_management as risk_api
import API.customer_insight as customer_api

client = TestClient(main.app)


def test_dashboard(monkeypatch):
    monkeypatch.setattr(api_dashboard, 'fetch_dashboard_data', lambda: {'metrics': [], 'charts': []})
    resp = client.get('/api/dashboard')
    assert resp.status_code == 200
    assert resp.json() == {'metrics': [], 'charts': []}


def test_financial_performance(monkeypatch):
    monkeypatch.setattr(financial_api, 'get_financial_performance_data', lambda ft, c: {'metrics': [], 'charts': []})
    resp = client.get('/api/financial-performance')
    assert resp.status_code == 200
    assert resp.json() == {'metrics': [], 'charts': []}


def test_operational_efficiency(monkeypatch):
    monkeypatch.setattr(operational_api, 'get_operational_efficiency_data', lambda ft, c: {'metrics': [], 'charts': []})
    resp = client.get('/api/operational-efficiency')
    assert resp.status_code == 200
    assert resp.json() == {'metrics': [], 'charts': []}


def test_demographic(monkeypatch):
    monkeypatch.setattr(demographic_api, 'get_demo_kpi_data', lambda ft, c: {'metrics': [], 'charts': []})
    resp = client.get('/api/demographic')
    assert resp.status_code == 200
    assert resp.json() == {'metrics': [], 'charts': []}


def test_risk_and_fraud(monkeypatch):
    monkeypatch.setattr(risk_api, 'get_risk_and_fraud_data', lambda ft, c: {'metrics': [], 'charts': []})
    resp = client.get('/api/risk-and-fraud')
    assert resp.status_code == 200
    assert resp.json() == {'metrics': [], 'charts': []}


def test_customer_insights(monkeypatch):
    monkeypatch.setattr(customer_api, 'get_customer_insights_data', lambda ft, c: {'metrics': [], 'charts': []})
    resp = client.get('/api/customer-insights')
    assert resp.status_code == 200
    assert resp.json() == {'metrics': [], 'charts': []}
