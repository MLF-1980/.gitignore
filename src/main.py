import os
import sqlite3
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from src.web.web_routes import router as web_router

app = FastAPI(title="SafeCore API")

DB_PATH = "safecore.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS personnel (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            dni TEXT NOT NULL,
            company TEXT NOT NULL,
            medical_clearance TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            incident_date TEXT NOT NULL,
            project_name TEXT NOT NULL,
            injured_name TEXT NOT NULL,
            person_type TEXT NOT NULL,
            description TEXT NOT NULL,
            lost_days INTEGER NOT NULL,
            severity_type TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()

@app.on_event("startup")
def startup_event():
    init_db()

# Rutas absolutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Montar estáticos
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Incluir router web/excel
app.include_router(web_router)

# Modelos Pydantic para API JSON
class IncidentModel(BaseModel):
    incident_date: str
    project_name: str
    injured_name: str
    person_type: str
    description: str
    lost_days: int
    severity_type: str

class PersonnelModel(BaseModel):
    full_name: str
    dni: str
    company: str
    medical_clearance: str
    status: str

@app.get("/")
async def read_root():
    return FileResponse(os.path.join(STATIC_DIR, "app_demo.html"))

@app.get("/api/incidents")
async def get_incidents():
    conn = get_db_connection()
    rows = [dict(row) for row in conn.cursor().execute("SELECT * FROM incidents").fetchall()]
    conn.close()
    return rows

@app.post("/api/incidents")
async def create_incident(data: IncidentModel):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO incidents (incident_date, project_name, injured_name, person_type, description, lost_days, severity_type) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (data.incident_date, data.project_name, data.injured_name, data.person_type, data.description, data.lost_days, data.severity_type)
    )
    conn.commit()
    conn.close()
    return {"status": "success"}

@app.get("/api/personnel")
async def get_personnel():
    conn = get_db_connection()
    rows = [dict(row) for row in conn.cursor().execute("SELECT * FROM personnel").fetchall()]
    conn.close()
    return rows

@app.post("/api/personnel")
async def create_personnel(data: PersonnelModel):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO personnel (full_name, dni, company, medical_clearance, status) VALUES (?, ?, ?, ?, ?)",
        (data.full_name, data.dni, data.company, data.medical_clearance, data.status)
    )
    conn.commit()
    conn.close()
    return {"status": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)