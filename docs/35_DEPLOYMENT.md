# 35. Deployment

## 1. Local Development & Demonstration Setup
Crowd Flow is designed for zero-friction local execution on Windows 10/11 or Linux:

### 1.1 Backend Setup
```powershell
# Navigate to backend directory
cd backend

# Create and activate Python virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install required dependencies
pip install -r requirements.txt

# Run database migrations and seed default network
python -m app.database.init_db

# Launch FastAPI development server
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 1.2 Frontend Setup
```powershell
# Navigate to frontend directory
cd frontend

# Install Node dependencies
npm install

# Start Vite React development server
npm run dev
```

### 1.3 Accessing the Application
- **Operator Dashboard:** `http://localhost:5173`
- **Interactive API Documentation:** `http://127.0.0.1:8000/docs` (Swagger UI)
- **Default Credentials:**
  - Admin: `admin` / `admin123`
  - Operator: `operator` / `operator123`
