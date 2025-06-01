#debian image with python 3.12 and pip
FROM python:3.12-slim	
#setting the working directory (inside) the container to /app
#now the next commands (COPY, RUN, CMD) now happen from /app
WORKDIR /app
#installing the minimum dependencies to run the app
RUN apt-get update && \
    apt-get install -y build-essential && \
    rm -rf /var/lib/apt/lists/*


#copying the requirements.txt file to the working directory
COPY requirements.txt .

#installing the python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt
#copying the rest of the files to the working directory
COPY . .

# declare port 8000 to be used by the container FastAPI default 8000 port
#    - This is for documentation; doesn’t open the port by itself
EXPOSE 8000
# prevent Python from buffering stdout/stderr
#  Ensures you see real time logs with `docker logs`
ENV PYTHONUNBUFFERED=1
# define the command that runs when the container starts
#     - Launches your FastAPI app using Uvicorn
#     - `"app.main:app"` means: file `main.py` inside `app/` folder, with a `FastAPI()` instance called `app`
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]