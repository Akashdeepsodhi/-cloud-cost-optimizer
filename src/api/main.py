"""
Main FastAPI application for Cloud Cost Optimizer
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime

app = FastAPI(
    title="Cloud Cost Optimizer - India",
    description="Cloud cost optimization platform for the Indian market",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class HealthCheck(BaseModel):
    status: str
    version: str
    market: str
    currency: str
    timestamp: datetime

class CostSummary(BaseModel):
    total_cost_inr: float
    monthly_cost_inr: float
    potential_savings_inr: float
    optimization_score: int
    last_updated: datetime

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>Cloud Cost Optimizer - India</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                .container { max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; }
                .header { text-align: center; margin-bottom: 30px; }
                .header h1 { color: #FF6B35; }
                .links { text-align: center; margin-top: 30px; }
                .links a { margin: 0 10px; padding: 12px 24px; background: #FF6B35; color: white; text-decoration: none; border-radius: 5px; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🇮🇳 Cloud Cost Optimizer for India</h1>
                    <p>Optimize your cloud costs with Indian market solutions</p>
                </div>
                <div class="links">
                    <a href="/docs">API Documentation</a>
                    <a href="/api/v1/health">Health Check</a>
                </div>
            </div>
        </body>
    </html>
    """

@app.get("/api/v1/health", response_model=HealthCheck)
async def health_check():
    return HealthCheck(
        status="healthy",
        version="1.0.0",
        market="India",
        currency="INR",
        timestamp=datetime.now()
    )

@app.get("/api/v1/summary", response_model=CostSummary)
async def get_cost_summary():
    return CostSummary(
        total_cost_inr=125000.0,
        monthly_cost_inr=85000.0,
        potential_savings_inr=30000.0,
        optimization_score=75,
        last_updated=datetime.now()
    )

@app.get("/api/v1/pricing/india")
async def get_indian_pricing():
    return {
        "currency": "INR",
        "tiers": {
            "freemium": {"monthly_fee": 0, "max_monthly_spend": 800000},
            "starter": {"monthly_fee": 8000, "max_annual_spend": 8000000},
            "growth": {"monthly_fee": 15000, "max_annual_spend": 20000000},
            "enterprise": {"percentage_fee": 1.5}
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
