"""
Test API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["market"] == "India"
    assert data["currency"] == "INR"

def test_cost_summary():
    response = client.get("/api/v1/summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_cost_inr" in data
    assert "potential_savings_inr" in data

def test_indian_pricing():
    response = client.get("/api/v1/pricing/india")
    assert response.status_code == 200
    data = response.json()
    assert data["currency"] == "INR"
    assert "tiers" in data
