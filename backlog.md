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
- [x] Tests del formulario de contacto — 8/8 pasando (pytest + httpx)
- [x] Auditoría re-corrida: gitleaks OK, trivy 0 CVEs (jinja2→3.1.6), bandit limpio, semgrep limpio
- [x] Análisis del modelo de negocio documentado (`docs/analisis-modelo-negocio.md`): 13 documentos de `sources/`, 6 modelos de negocio, posibilidades y gaps
- [x] Tarifas completas publicadas en `/servicios` (8 segmentos × 3 niveles + servicios individuales)
- [x] Página `/proyectos` con casos de éxito reales (The Top, El Kazurro, El Patioh) + teaser en home

## 🔲 Pendiente

### Datos de contacto (bloquea footer, WhatsApp y el "punto final" de la web)
- [ ] Rellenar teléfono, email, ciudad y redes en `base.html` footer
- [ ] Definir número de WhatsApp en `static/js/main.js` (activa el botón flotante)
- [ ] Número corporativo real para el botón flotante
- [ ] Confirmar con Lau las cifras exactas y el permiso de publicación de los casos de éxito (`/proyectos`) — el PDF fuente (`CREAS-AGENCY.pdf`) tiene el texto corrupto y las métricas están marcadas como pendientes en el template
- [ ] Email corporativo: cuando exista dominio, `hola@qreasagency.com` (Google Workspace o Zoho). La cuenta `qreas.agency@gmail.com` ya está creada para administrar Search Console / GA4 y el Workspace. En desarrollo no se paga nada

### Despliegue
- [ ] (Más adelante) VPS + dominio + HTTPS en `qreasagency.com`

### Calidad / mantenimiento
- [ ] Enviar sitemap a Google Search Console cuando esté pública
- [ ] Migrar leads de SQLite a CRM / ERP QreasTech cuando se decida
- [ ] Revisar añadir pre-commit (ruff+bandit) y CI de GitHub Actions cuando el código crezca — hoy no aporta (main.py pequeño, ruff y pytest ya verdes)

## 🧭 Notas

- `leads.db` se crea solo al arrancar; está en `.gitignore` y en el volumen de Docker (sobrevive a reinicios).
- `backlog.md` y `docs/backlog.html` son la MISMA cosa en dos formatos: el md es la versión de trabajo (fácil de editar) y el html la versión "vitaminada" que ve Lau. Mantenerlos sincronizados.
- Naming confirmado con Lau: **QREA'S Agency** (con Q y apóstrofo). Los documentos antiguos de `sources/` usan "CREA'S" porque son del proyecto original de hace un año. El caso de éxito es **El Kazurro** (con K), no "Cazurro".
- Identidad visual intocada: dorado bronce, Source Serif 4 y logos son trabajo pulido en Adobe, aprobado. No sustituir por genéricos.
- Tarifas y paquetes: datos editables en `main.py` (`PACKAGES`, `INDIVIDUAL_SERVICES`).
- Análisis de los documentos de negocio: `docs/analisis-modelo-negocio.md` (13 documentos, 6 modelos de negocio).
- Sin CLAUDE.md todavía — crear uno si el proyecto crece o se vuelve colaborativo.
