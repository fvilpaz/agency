from pathlib import Path
import sqlite3
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, EmailStr
from typing import List

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "leads.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            apellidos TEXT,
            negocio TEXT,
            ciudad TEXT,
            email TEXT,
            telefono TEXT,
            tipo TEXT,
            momento TEXT,
            mejoras TEXT,
            mensaje TEXT,
            privacidad INTEGER,
            created_at TEXT DEFAULT (datetime('now'))
        )
        """
    )
    conn.commit()
    conn.close()


init_db()

app = FastAPI(title="QREA'S Agency")

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

class ContactForm(BaseModel):
    nombre: str
    apellidos: str | None = None
    negocio: str
    ciudad: str | None = None
    email: EmailStr
    telefono: str | None = None
    tipo: str | None = None
    momento: str | None = None
    mejoras: List[str] = []
    mensaje: str | None = None
    privacidad: bool = False

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/servicios")
async def servicios(request: Request):
    return templates.TemplateResponse(request=request, name="servicios.html")

@app.get("/metodo")
async def metodo(request: Request):
    return templates.TemplateResponse(request=request, name="metodo.html")

@app.get("/tecnologia-hosteleria")
async def tecnologia(request: Request):
    return templates.TemplateResponse(request=request, name="tecnologia.html")

@app.get("/contacto")
async def contacto(request: Request):
    return templates.TemplateResponse(request=request, name="contacto.html")

@app.post("/contacto")
async def submit_contacto(form: ContactForm):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO leads (nombre, apellidos, negocio, ciudad, email, telefono, tipo, momento, mejoras, mensaje, privacidad) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            form.nombre,
            form.apellidos,
            form.negocio,
            form.ciudad,
            form.email,
            form.telefono,
            form.tipo,
            form.momento,
            ", ".join(form.mejoras),
            form.mensaje,
            int(form.privacidad),
        ),
    )
    conn.commit()
    conn.close()
    return JSONResponse({"ok": True, "message": "Gracias. Hemos recibido tu solicitud y te contactaremos en breve."})

@app.get("/politica-de-privacidad")
async def privacidad(request: Request):
    return templates.TemplateResponse(request=request, name="legal/privacidad.html")

@app.get("/aviso-legal")
async def aviso_legal(request: Request):
    return templates.TemplateResponse(request=request, name="legal/aviso_legal.html")

@app.get("/politica-de-cookies")
async def cookies(request: Request):
    return templates.TemplateResponse(request=request, name="legal/cookies.html")

@app.get("/robots.txt")
async def robots():
    return FileResponse(BASE_DIR / "static" / "robots.txt")

@app.get("/sitemap.xml")
async def sitemap():
    return FileResponse(BASE_DIR / "static" / "sitemap.xml")
