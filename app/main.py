from fastapi import FastAPI
from app.routes import route_worker
from app.routes import route_schedule
from app.routes import route_logger
from fastapi.middleware.cors import CORSMiddleware


 
app = FastAPI()
app.include_router(route_worker.router)
app.include_router(route_schedule.router)
app.include_router(route_logger.router)

    # its avoid  a raising error with dotenv when running the app with uvicorn command from terminal.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://script.google.com", "https://docs.google.com"],
    allow_credentials=True,
    allow_methods=["POST"],  # or limit to ["POST", "GET"]
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to the scheduler API!"}