from fastapi import FastAPI
from .routes.route_worker import router
 
 
app = FastAPI()
app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Welcome to the scheduler API!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True) # This line is used to run the FastAPI app with Uvicorn server.
    # its avoid  a raising error with dotenv when running the app with uvicorn command from terminal.
    