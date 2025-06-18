from fastapi import FastAPI, Depends
from app.routes import route_worker
from app.routes import route_schedule
from app.routes import route_logger
from fastapi.middleware.cors import CORSMiddleware
from app.services.api_key import get_api_key


app = FastAPI()

# Add API key dependency to all routes
app.dependency_overrides[get_api_key] = get_api_key

app.include_router(route_worker.router, dependencies=[Depends(get_api_key)])
app.include_router(route_schedule.router, dependencies=[Depends(get_api_key)])
app.include_router(route_logger.router, dependencies=[Depends(get_api_key)])

    # its avoid  a raising error with dotenv when running the app with uvicorn command from terminal.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://script.google.com", "https://docs.google.com"], # Allow Google Apps Script and Google Docs origins 
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to the scheduler API!"}