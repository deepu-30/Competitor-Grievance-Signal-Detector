import json
import sqlite3
import os
from datetime import datetime

def save_json(signals, path="outputs/signals.json"):
    """Save all signals to a JSON file."""
    os.makedirs("outputs", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(signals, f, indent=2, ensure_ascii=False)
    print(f"\n✅ Saved {len(signals)} signals → {path}")

def save_sqlite(signals, db_path="outputs/signals.db"):
    """Save all signals to a SQLite database."""
    os.makedirs("outputs", exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS signals (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            company         TEXT,
            signal_type     TEXT,
            source_url      TEXT,
            source          TEXT,
            matched_keywords TEXT,
            pain_points     TEXT,
            signal_score    INTEGER,
            detected_at     TEXT,
            reason          TEXT
        )
    """)
    for s in signals:
        conn.execute(
            "INSERT INTO signals VALUES (NULL,?,?,?,?,?,?,?,?,?)",
            (
                s["company"],
                s["signal_type"],
                s["source_url"],
                s["source"],
                json.dumps(s["matched_keywords"]),
                json.dumps(s["pain_points"]),
                s["signal_score"],
                s["detected_at"],
                s["reason"]
            )
        )
    conn.commit()
    conn.close()
    print(f"✅ Saved {len(signals)} signals → {db_path}")