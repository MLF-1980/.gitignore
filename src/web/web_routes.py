from fastapi import APIRouter, Request, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
import pandas as pd
import sqlite3
import os

router = APIRouter(tags=["Web Views"])
DB_PATH = "safecore.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@router.post("/api/import-excel")
async def import_excel_route(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Archivo no seleccionado")
    try:
        contents = await file.read()
        import io
        df = pd.read_excel(io.BytesIO(contents))
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO incidents (incident_date, project_name, injured_name, person_type, description, lost_days, severity_type)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                str(row.get("Fecha", "")),
                str(row.get("Proyecto", "")),
                str(row.get("Afectado", "")),
                str(row.get("Tipo", "")),
                str(row.get("Descripción", "")),
                int(row.get("Días Perdidos", 0)),
                str(row.get("Gravedad", ""))
            ))
        
        conn.commit()
        conn.close()
        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el archivo Excel: {e}")