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

PACKAGES = [
    {
        "id": "bares-tapas",
        "name": "Bares de Tapas y Tabernas",
        "tiers": [
            {"level": "Básico", "tone": "green", "price": "600 – 1.000 €", "includes": ["Diseño de menú", "Escandallos", "Optimización de costos"]},
            {"level": "Intermedio", "tone": "blue", "price": "1.500 – 2.500 €", "includes": ["Branding", "Gestión de proveedores", "Manual de operación"], "base": "Básico"},
            {"level": "Premium", "tone": "gold", "price": "3.000 – 5.000 €", "includes": ["Formación en servicio", "Optimización de procesos", "Fidelización"], "base": "Intermedio"},
        ],
    },
    {
        "id": "copas-cocteleria",
        "name": "Bares de Copas y Coctelerías",
        "tiers": [
            {"level": "Básico", "tone": "green", "price": "700 – 1.200 €", "includes": ["Diseño de carta de cócteles", "Escandallos", "Control de costos"]},
            {"level": "Intermedio", "tone": "blue", "price": "1.800 – 3.000 €", "includes": ["Branding", "Optimización de barra y servicio"], "base": "Básico"},
            {"level": "Premium", "tone": "gold", "price": "3.500 – 6.000 €", "includes": ["Formación de bartenders", "Estrategia de eventos", "Automatización"], "base": "Intermedio"},
        ],
    },
    {
        "id": "restaurantes-casual",
        "name": "Restaurantes Casual y Gastrobares",
        "tiers": [
            {"level": "Básico", "tone": "green", "price": "900 – 1.500 €", "includes": ["Manuales operativos", "Escandallos", "Optimización de menú"]},
            {"level": "Intermedio", "tone": "blue", "price": "2.500 – 4.000 €", "includes": ["Estrategia de precios", "Control de costos", "Branding"], "base": "Básico"},
            {"level": "Premium", "tone": "gold", "price": "5.000 – 8.000 €", "includes": ["Formación de equipo", "Optimización de sala y cocina"], "base": "Intermedio"},
        ],
    },
    {
        "id": "alta-gama",
        "name": "Restaurantes de Alta Gama y Estrella Michelin",
        "tiers": [
            {"level": "Básico", "tone": "green", "price": "1.500 – 3.000 €", "includes": ["Optimización de costos", "Análisis financiero", "Escandallos premium"]},
            {"level": "Intermedio", "tone": "blue", "price": "4.000 – 7.000 €", "includes": ["Diseño de experiencia gastronómica", "Branding de lujo"], "base": "Básico"},
            {"level": "Premium", "tone": "gold", "price": "8.000 – 15.000 €", "includes": ["Formación avanzada", "Protocolo de servicio", "Auditoría operativa"], "base": "Intermedio"},
        ],
    },
    {
        "id": "hoteles-resorts",
        "name": "Hoteles y Resorts",
        "tiers": [
            {"level": "Básico", "tone": "green", "price": "2.000 – 4.000 €", "includes": ["Manual de atención al huésped", "Optimización de bufé", "Room service"]},
            {"level": "Intermedio", "tone": "blue", "price": "5.000 – 8.000 €", "includes": ["Análisis financiero", "Estrategias de fidelización", "Servicio"], "base": "Básico"},
            {"level": "Premium", "tone": "gold", "price": "10.000 – 20.000 €", "includes": ["Automatización", "Gestión de eventos", "Formación de personal"], "base": "Intermedio"},
        ],
    },
    {
        "id": "fast-food",
        "name": "Fast Food y Franquicias",
        "tiers": [
            {"level": "Básico", "tone": "green", "price": "1.200 – 2.000 €", "includes": ["Estandarización de procesos", "Manual de operación"]},
            {"level": "Intermedio", "tone": "blue", "price": "3.500 – 6.000 €", "includes": ["Control de costos", "Optimización de compras", "Branding"], "base": "Básico"},
            {"level": "Premium", "tone": "gold", "price": "8.000 – 12.000 €", "includes": ["Estrategia de franquicia", "Automatización de procesos"], "base": "Intermedio"},
        ],
    },
    {
        "id": "eventos-catering",
        "name": "Eventos y Catering",
        "tiers": [
            {"level": "Básico", "tone": "green", "price": "800 – 1.500 €", "includes": ["Planificación básica", "Escandallos", "Proveedores"]},
            {"level": "Intermedio", "tone": "blue", "price": "2.500 – 4.500 €", "includes": ["Branding", "Estrategia de precios", "Formación de equipo"], "base": "Básico"},
            {"level": "Premium", "tone": "gold", "price": "5.000 – 10.000 €", "includes": ["Gestión integral del evento", "Automatización", "Fidelización"], "base": "Intermedio"},
        ],
    },
    {
        "id": "cafeterias",
        "name": "Cafeterías y Coffee Shops",
        "tiers": [
            {"level": "Básico", "tone": "green", "price": "700 – 1.500 €", "includes": ["Diseño de menú", "Escandallos", "Optimización de productos"]},
            {"level": "Intermedio", "tone": "blue", "price": "2.000 – 4.000 €", "includes": ["Branding", "Estrategias de fidelización", "Control de costos"], "base": "Básico"},
            {"level": "Premium", "tone": "gold", "price": "4.500 – 7.500 €", "includes": ["Formación en experiencia de cliente", "Automatización"], "base": "Intermedio"},
        ],
    },
]

INDIVIDUAL_SERVICES = [
    {"name": "Diseño de menús y branding", "price": "Desde 500 €"},
    {"name": "Consultoría financiera y análisis de costos", "price": "Desde 700 €"},
    {"name": "Formación de personal", "price": "Desde 1.000 €"},
    {"name": "Gestión de eventos", "price": "Desde 1.500 €"},
    {"name": "Automatización y digitalización", "price": "Desde 2.000 €"},
]


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
    return templates.TemplateResponse(
        request=request,
        name="servicios.html",
        context={"segments": PACKAGES, "individual": INDIVIDUAL_SERVICES},
    )

@app.get("/metodo")
async def metodo(request: Request):
    return templates.TemplateResponse(request=request, name="metodo.html")

@app.get("/proyectos")
async def proyectos(request: Request):
    return templates.TemplateResponse(request=request, name="proyectos.html")

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
