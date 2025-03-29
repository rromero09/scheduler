from fastapi import FastAPI
from app.routes import route_worker
from app.routes import route_schedule

 
app = FastAPI()
app.include_router(route_worker.router)
app.include_router(route_schedule.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the scheduler API!"}

    # its avoid  a raising error with dotenv when running the app with uvicorn command from terminal.
