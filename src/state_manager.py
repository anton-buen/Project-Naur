import sqlite3
import logging
from pathlib import Path

logger = logging.getLogger("naur.state")

BASE_DIR = Path(__file__).parent.parent
DB_FILE = BASE_DIR / "naur_state.db"

def get_connection():
    # 15-second timeout handles parallel LLM tool calls
    conn = sqlite3.connect(DB_FILE, check_same_thread=False, timeout=15.0)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS chat_ledger
                        (id INTEGER PRIMARY KEY AUTOINCREMENT, role TEXT, content TEXT)''')
        # UPGRADED SCHEMA: Added business_impact column
        conn.execute('''CREATE TABLE IF NOT EXISTS domain_constraints
                        (domain TEXT PRIMARY KEY, constraint_text TEXT, business_impact TEXT, risk_level TEXT)''')
        conn.execute('''CREATE TABLE IF NOT EXISTS project_glossary
                        (term TEXT PRIMARY KEY, definition TEXT)''')

def append_message(role: str, content: str) -> bool:
    try:
        with get_connection() as conn:
            conn.execute("INSERT INTO chat_ledger (role, content) VALUES (?, ?)", (role, content))
        return True
    except sqlite3.Error as e:
        logger.error(f"[DB ERROR] Append message failed: {e}")
        return False

def get_chat_history() -> list[dict]:
    try:
        with get_connection() as conn:
            rows = conn.execute("SELECT role, content FROM chat_ledger ORDER BY id ASC").fetchall()
            return [{"role": r["role"], "content": r["content"]} for r in rows]
    except sqlite3.Error as e:
        return []

def update_constraint(domain: str, text: str, business_impact: str, risk: str) -> bool:
    valid_domains = ["PROD", "FE", "BE", "DS", "UI", "GLOBAL"]
    if domain not in valid_domains:
        return False
        
    try:
        with get_connection() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO domain_constraints (domain, constraint_text, business_impact, risk_level) VALUES (?, ?, ?, ?)",
                (domain, text, business_impact, risk)
            )
        return True
    except sqlite3.Error as e:
        logger.error(f"[DB ERROR] Update constraint failed: {e}")
        return False

def get_constraints() -> dict:
    try:
        with get_connection() as conn:
            rows = conn.execute("SELECT domain, constraint_text, business_impact, risk_level FROM domain_constraints").fetchall()
            return {r["domain"]: {"text": r["constraint_text"], "business": r["business_impact"], "risk": r["risk_level"]} for r in rows}
    except sqlite3.Error as e:
        return {}

def upsert_glossary_term(term: str, definition: str) -> bool:
    try:
        with get_connection() as conn:
            conn.execute("INSERT OR REPLACE INTO project_glossary (term, definition) VALUES (?, ?)", (term, definition))
        return True
    except sqlite3.Error as e:
        return False

def get_glossary() -> dict:
    try:
        with get_connection() as conn:
            rows = conn.execute("SELECT term, definition FROM project_glossary ORDER BY term ASC").fetchall()
            return {r["term"]: r["definition"] for r in rows}
    except sqlite3.Error as e:
        return {}

def clear_ledger() -> bool:
    try:
        with get_connection() as conn:
            conn.execute("DELETE FROM chat_ledger")
            conn.execute("DELETE FROM domain_constraints")
            conn.execute("DELETE FROM project_glossary")
        return True
    except sqlite3.Error as e:
        return False

init_db()