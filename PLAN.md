# PLAN — QREA'S Agency (web corporativa)

Stack: FastAPI · Jinja2 · SQLite · Docker
Repo: https://github.com/fvilpaz/agency (privado)

## ✅ Completado

- [x] Repo git + GitHub privado (`fvilpaz/agency`)
- [x] Formulario de contacto arreglado (adiós 422 JS↔pydantic)
- [x] Leads persistidos en SQLite (`leads.db`)
- [x] SEO: sitemap sin `.html`, JSON-LD, footer `#inicio` → `/`
- [x] `python-multipart` eliminada (4 CVEs HIGH del audit)
- [x] `convert_templates.py` archivado en `docs/_archivo/`
- [x] Dockerfile limpio para prod (`--reload` solo en dev)
- [x] Cursor custom fluido con rAF + reduced-motion
- [x] Despliegue con `cloudflared` verificado funcionando

## 🔲 Pendiente

### Datos de contacto (bloquea footer, WhatsApp y el "punto final" de la web)
- [ ] Rellenar teléfono, email, ciudad y redes en `base.html` footer
- [ ] Definir número de WhatsApp en `static/js/main.js` (activa el botón flotante)
- [ ] Número corporativo real para el botón flotante

### Despliegue
- [ ] (Más adelante) VPS + dominio + HTTPS en `qreasagency.com`

### Calidad / mantenimiento
- [ ] Re-correr `audit` (ahora con repo git, gitleaks ya escanea)
- [ ] Tests básicos con pytest para `POST /contacto` (200 + lead en BD)
- [ ] Enviar sitemap a Google Search Console cuando esté pública
- [ ] Migrar leads de SQLite a CRM / ERP QreasTech cuando se decida
- [ ] Mejorar `nando-toolkit`: detectar FastAPI en `audit-*.sh` (falso negativo actual)

## 🧭 Notas

- `leads.db` se crea solo al arrancar; está en `.gitignore` y en el volumen de Docker (sobrevive a reinicios).
- Sin CLAUDE.md todavía — crear uno si el proyecto crece o se vuelve colaborativo.
