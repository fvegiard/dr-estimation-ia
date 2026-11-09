"""Push data/dre.sqlite to Supabase: stage every table, then swap atomically (public.sync_commit).

Needs the project's service_role key (Supabase dashboard > Project Settings > API keys), read from
the SUPABASE_SERVICE_ROLE_KEY environment variable or a `.env` file in the project root (git-ignored).
"""
from __future__ import annotations

import os
import sqlite3
import sys
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from dre_estimation.search import SYNONYMS  # noqa: E402

URL = "https://wirmffxgipmsbuuxufwk.supabase.co"
TABLES = ["products", "assemblies", "assembly_components", "unit_ratios", "units", "labor_rates", "meta"]
BATCH = 2000


def service_key() -> str:
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
    env = ROOT / ".env"
    if not key and env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            if line.startswith("SUPABASE_SERVICE_ROLE_KEY="):
                key = line.split("=", 1)[1].strip().strip('"')
    if not key:
        sys.exit("SUPABASE_SERVICE_ROLE_KEY not set (env var or .env) - see docstring")
    return key


def main():
    key = service_key()
    con = sqlite3.connect(ROOT / "data" / "dre.sqlite")
    con.row_factory = sqlite3.Row
    client = httpx.Client(base_url=URL + "/rest/v1", timeout=300,
                          headers={"apikey": key, "Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    data = {t: [dict(r) for r in con.execute(f"SELECT * FROM {t}")] for t in TABLES}
    data["synonyms"] = [{"word": w, "grp": g} for g, words in enumerate(SYNONYMS) for w in dict.fromkeys(words)]
    for tbl, rows in data.items():
        for i in range(0, max(len(rows), 1), BATCH):
            r = client.post("/rpc/sync_stage_rows", json={"tbl": tbl, "rows": rows[i:i + BATCH], "reset": i == 0})
            r.raise_for_status()
        print(f"staged {tbl}: {len(rows)}")
    r = client.post("/rpc/sync_commit", json={"expect": {t: len(rows) for t, rows in data.items()}})
    r.raise_for_status()
    print("cloud catalog replaced:", r.json())


if __name__ == "__main__":
    main()
