# 📦 FastAPI Scheduler App

This project is a backend service built with FastAPI, designed to generate worker schedules, storage log events in MongoDB, and be deployed thru Docker 

---

## To run the server (without Docker)

### 1. Create and activate virtual environment (optional but recommended):
```bash
python3 -m venv .venv
source venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Getting the dependencies
optional but recommended (uv pip)
```bash
    pip install uv
````
and then just write uv before every pip
```bash
pip install -r requirements.txt


```

### 3. Set environment variables:
Make sure you have a `.env` file at the root:
```env
MONGO_URI=mongodb://localhost:27017
DB_NAME=scheduler_db
LOG_COLLECTION=logs
```

### 4. Run the FastAPI app with Uvicorn:
```bash
uvicorn app.main:app --reload
```

### 5. Open in browser:
Visit [http://localhost:8000/docs](http://localhost:8000/docs) for the interactive doc that FastAPI offer for free

---

## 🐳 Running the App with Docker Compose

### 1. Build and start services:
```bash
docker-compose up --build
```

This will:
- Build the FastAPI app image
- Start MongoDB with authentication
- Connect them via an internal Docker network

### 2. Access the app:
Visit [http://localhost:8000/docs](http://localhost:8000/docs)

### Optional: Access MongoDB from MongoDB Compass:
Use this connection string:
```text
mongodb://rarr:25886688@localhost:27017/?authSource=admin
```

---

## 📁 Folder Structure (Example)
```
project-root/
├── app/
│   ├── main.py
│   ├── routes/
│   ├── services/
│   └── db/
├── .env
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 🧹 Stopping and Cleaning Up

### Stop the containers:
```bash
docker-compose down
```

### Stop and remove volumes:
```bash
docker-compose down -v
```

---

## ✅ Notes
- Make sure Docker Desktop is running.
- `.env` file must be in the root and readable.
- MongoDB data is stored in a volume named `mongo_data`.

Let me know if you need help customizing this for production or cloud deployment!
