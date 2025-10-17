"""
Main FastAPI application for Cloud Cost Optimizer
"""
from fastapi import Depends, FastAPI, Form, HTTPException, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from src.api.deps import COOKIE_NAME, get_current_user
from src.core.database import Base, engine, get_db
from src.core.security import create_access_token, get_password_hash, verify_password
from src.models.user import User

app = FastAPI(
    title="Cloud Cost Optimizer - India",
    description="Cloud cost optimization platform for the Indian market",
    version="1.0.0"
)

# Create tables on startup
@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


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
async def root(request: Request):
    return f"""
    <html>
        <head>
            <title>Cloud Cost Optimizer - India</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
                .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; }}
                .header {{ text-align: center; margin-bottom: 30px; }}
                .header h1 {{ color: #FF6B35; }}
                .links {{ text-align: center; margin-top: 30px; }}
                .links a {{ margin: 0 10px; padding: 12px 24px; background: #FF6B35; color: white; text-decoration: none; border-radius: 5px; }}
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
                    <a href="/login">Login</a>
                    <a href="/register">Register</a>
                    <a href="/dashboard">Dashboard</a>
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


# --------------------- Auth Pages & Routes ---------------------

@app.get("/register", response_class=HTMLResponse)
async def register_form():
    return """
    <html>
      <head>
        <title>Register</title>
        <style>
          body { font-family: Arial, sans-serif; background:#f5f5f5; padding:40px; }
          .card { max-width:420px; margin:0 auto; background:#fff; padding:28px; border-radius:10px; box-shadow: 0 2px 8px rgba(0,0,0,.08); }
          h2 { text-align:center; color:#FF6B35; }
          label { display:block; margin:10px 0 6px; }
          input { width:100%; padding:10px; border:1px solid #ddd; border-radius:6px; }
          button { margin-top:16px; width:100%; padding:12px; background:#FF6B35; color:#fff; border:none; border-radius:6px; cursor:pointer; }
          .alt { text-align:center; margin-top:10px; }
        </style>
      </head>
      <body>
        <div class="card">
          <h2>Create account</h2>
          <form method="post" action="/register">
            <label for="full_name">Full name</label>
            <input id="full_name" name="full_name" type="text" />
            <label for="email">Email</label>
            <input id="email" name="email" type="email" required />
            <label for="password">Password</label>
            <input id="password" name="password" type="password" required />
            <button type="submit">Register</button>
          </form>
          <div class="alt"><a href="/login">Already have an account? Login</a></div>
        </div>
      </body>
    </html>
    """


@app.post("/register")
def register(
    email: str = Form(...),
    password: str = Form(...),
    full_name: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user = User(email=email, full_name=full_name, hashed_password=get_password_hash(password))
    db.add(user)
    db.commit()
    response = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    return response


@app.get("/login", response_class=HTMLResponse)
async def login_form():
    return """
    <html>
      <head>
        <title>Login</title>
        <style>
          body { font-family: Arial, sans-serif; background:#f5f5f5; padding:40px; }
          .card { max-width:420px; margin:0 auto; background:#fff; padding:28px; border-radius:10px; box-shadow: 0 2px 8px rgba(0,0,0,.08); }
          h2 { text-align:center; color:#FF6B35; }
          label { display:block; margin:10px 0 6px; }
          input { width:100%; padding:10px; border:1px solid #ddd; border-radius:6px; }
          button { margin-top:16px; width:100%; padding:12px; background:#FF6B35; color:#fff; border:none; border-radius:6px; cursor:pointer; }
          .alt { text-align:center; margin-top:10px; }
        </style>
      </head>
      <body>
        <div class="card">
          <h2>Welcome back</h2>
          <form method="post" action="/login">
            <label for="email">Email</label>
            <input id="email" name="email" type="email" required />
            <label for="password">Password</label>
            <input id="password" name="password" type="password" required />
            <button type="submit">Login</button>
          </form>
          <div class="alt"><a href="/register">Create an account</a></div>
        </div>
      </body>
    </html>
    """


@app.post("/login")
def login(
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")
    token = create_access_token(subject=user.email)
    # Set HTTP-only cookie
    response = RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        httponly=True,
        samesite="lax",
        max_age=60 * 60 * 24,
        secure=False,
        path="/",
    )
    return response


@app.get("/logout")
def logout():
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(COOKIE_NAME, path="/")
    return response


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(user: User = Depends(get_current_user)):
    return f"""
    <html>
      <head>
        <title>Dashboard</title>
        <style>
          body {{ font-family: Arial, sans-serif; background:#f5f5f5; padding:40px; }}
          .card {{ max-width:900px; margin:0 auto; background:#fff; padding:28px; border-radius:10px; box-shadow: 0 2px 8px rgba(0,0,0,.08); }}
          .top {{ display:flex; align-items:center; justify-content:space-between; }}
          .btn {{ display:inline-block; padding:10px 16px; background:#FF6B35; color:#fff; text-decoration:none; border-radius:6px; }}
        </style>
      </head>
      <body>
        <div class="card">
          <div class="top">
            <h2>Hi {user.full_name or user.email}!</h2>
            <a class="btn" href="/logout">Logout</a>
          </div>
          <p>Welcome to your dashboard.</p>
          <p>Check the <a href="/api/v1/summary">cost summary API</a>.</p>
        </div>
      </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
