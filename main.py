from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import routers
from backend.app.api import startups, founders, auth, invitations, cofounder
from backend.app.database import engine
from backend.app.models import Base

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Startup Intelligence Platform",
    description="AI-Powered Startup Validation Platform",
    version="0.1.0"
)

# CORS middleware (allows frontend to call backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"], # Add both
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(invitations.router) 
app.include_router(cofounder.router)
app.include_router(startups.router)
app.include_router(founders.router)

@app.get("/")
async def root():
    return {
        "message": "Startup Intelligence Platform API",
        "version": "0.1.0",
        "endpoints": [
            "/api/auth/register",
            "/api/auth/login",
            "/api/auth/me",
            "/api/invitations",
            "/api/cofounder",
            "/api/startups",
            "/api/founders",
            "/health"
        ]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected"}

# Pydantic model for startup creation
class StartupCreate(BaseModel):
    name: str
    industry: str
    problem_statement: str
    solution: str
    #

@app.post("/startups/")
async def create_startup(startup: StartupCreate):
    return {
        "message": f"Startup {startup.name} created!",
        "data": startup
    }

@app.get("/startups/{startup_id}")
async def get_startup(startup_id: int):
    return {"startup_id": startup_id, "name": f"Startup {startup_id}"}

@app.put("/startups/{startup_id}")
async def update_startup(startup_id: int, startup: StartupCreate):
    return {
        "message": f"Startup {startup_id} updated!",
        "updated_data": startup
    }

@app.delete("/startups/{startup_id}")
async def delete_startup(startup_id: int):
    return {"message": f"Startup {startup_id} deleted!"}

@app.get("/search/")
async def search_startups(q: str, limit: int = 10):
    return {
        "search_term": q,
        "limit": limit,
        "results": []  # We'll add real data later
    }
#python -m uvicorn main:app --reload
