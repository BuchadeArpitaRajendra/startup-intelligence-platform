from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Startup Intelligence Platform")

class StartupCreate(BaseModel):
    name: str
    industry: str
    problem_statement: str
    solution: str

@app.get("/")
async def root():
    return {"message": "Hello World! Startup Intelligence Platform is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/startups/{startup_id}")
async def get_startup(startup_id: int):
    return {"startup_id": startup_id, "name": f"Startup {startup_id}"}
#python -m uvicorn main:app --reload

@app.post("/startups/")
async def create_startup(startup: StartupCreate):
    return {
        "message": f"Startup {startup.name} created!",
        "data": startup
    }
