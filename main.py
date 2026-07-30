from fastapi import FastAPI

app = FastAPI(title="Startup Intelligence Platform")

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
