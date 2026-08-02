import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import main


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "DB_PATH", tmp_path / "test_leads.db")
    main.init_db()
    with TestClient(main.app) as c:
        yield c


@pytest.fixture()
def get_leads(client):
    def _get(limit=10):
        conn = main.sqlite3.connect(main.DB_PATH)
        conn.row_factory = main.sqlite3.Row
        rows = conn.execute("SELECT * FROM leads ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        conn.close()
        return rows

    return _get
