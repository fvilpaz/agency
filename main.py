from pathlib import Path
from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, EmailStr
from typing import List

BASE_DIR = Path(__file__).parent

app = FastAPI(title="QREA'S Agency")

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

class ContactForm(BaseModel):
    nombre: str
    apellidos: str
    negocio: str
    ciudad: str
    email: EmailStr
    telefono: str
    tipo_negocio: str
    momento_proyecto: str
    mejoras: List[str]
    mensaje: str
    privacidad: bool

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
    # TODO: conectar a CRM / email cuando se confirme la herramienta
    print(f"[Lead] {form.nombre} {form.apellidos} <{form.email}> — {form.negocio}")
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
