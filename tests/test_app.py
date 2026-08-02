def test_home_ok(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "QREA" in r.text


def test_paginas_principales_ok(client):
    for ruta in ("/servicios", "/metodo", "/tecnologia-hosteleria", "/contacto"):
        r = client.get(ruta)
        assert r.status_code == 200, f"{ruta} devolvió {r.status_code}"


def test_paginas_legales_ok(client):
    for ruta in ("/politica-de-privacidad", "/aviso-legal", "/politica-de-cookies"):
        r = client.get(ruta)
        assert r.status_code == 200, f"{ruta} devolvió {r.status_code}"


def test_robots_y_sitemap_ok(client):
    assert client.get("/robots.txt").status_code == 200
    assert client.get("/sitemap.xml").status_code == 200


def test_contacto_valido_guarda_lead(client, get_leads):
    r = client.post(
        "/contacto",
        json={
            "nombre": "Luis",
            "apellidos": "García",
            "negocio": "La Taberna",
            "ciudad": "Vigo",
            "email": "luis@ejemplo.com",
            "telefono": "600123456",
            "tipo": "restaurante",
            "momento": "3_meses",
            "mejoras": ["operativa", "equipo"],
            "mensaje": "Quiero ordenar la operativa.",
            "privacidad": True,
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["ok"] is True

    leads = get_leads()
    assert len(leads) == 1
    lead = leads[0]
    assert lead["nombre"] == "Luis"
    assert lead["negocio"] == "La Taberna"
    assert lead["email"] == "luis@ejemplo.com"
    assert lead["mejoras"] == "operativa, equipo"
    assert lead["privacidad"] == 1


def test_contacto_sin_campos_obligatorios_422(client):
    r = client.post("/contacto", json={"nombre": "Solo nombre"})
    assert r.status_code == 422


def test_contacto_email_invalido_422(client):
    r = client.post(
        "/contacto",
        json={"nombre": "Ana", "negocio": "Bar", "email": "no-es-un-email"},
    )
    assert r.status_code == 422


def test_contacto_sin_privacidad_guardada_como_false(client, get_leads):
    r = client.post(
        "/contacto",
        json={
            "nombre": "María",
            "negocio": "Cafetería",
            "email": "maria@ejemplo.com",
            "privacidad": False,
        },
    )
    assert r.status_code == 200
    assert get_leads()[0]["privacidad"] == 0
