import sqlite3
import logging
from pathlib import Path

logger = logging.getLogger("naur.state")

BASE_DIR = Path(__file__).parent.parent
DB_FILE = BASE_DIR / "naur_state.db"

def get_connection():
    """Returns a connection to the SQLite database."""
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database schema."""
    with get_connection() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS chat_ledger
                        (id INTEGER PRIMARY KEY AUTOINCREMENT, role TEXT, content TEXT)''')
        conn.execute('''CREATE TABLE IF NOT EXISTS domain_constraints
                        (domain TEXT PRIMARY KEY, constraint_text TEXT, risk_level TEXT)''')
        conn.execute('''CREATE TABLE IF NOT EXISTS project_glossary
                        (term TEXT PRIMARY KEY, definition TEXT)''')

def append_message(role: str, content: str) -> bool:
    """Appends a message to the chat ledger."""
    try:
        with get_connection() as conn:
            conn.execute("INSERT INTO chat_ledger (role, content) VALUES (?, ?)", (role, content))
        return True
    except sqlite3.Error as e:
        logger.error(f"[DB ERROR] Append message failed: {e}")
        return False

def get_chat_history() -> list[dict]:
    """Retrieves all chat messages chronologically."""
    try:
        with get_connection() as conn:
            rows = conn.execute("SELECT role, content FROM chat_ledger ORDER BY id ASC").fetchall()
            return [{"role": r["role"], "content": r["content"]} for r in rows]
    except sqlite3.Error as e:
        logger.error(f"[DB ERROR] Fetch chat failed: {e}")
        return []

def update_constraint(domain: str, text: str, risk: str) -> bool:
    """Updates a domain constraint, permitting all 5 domains plus GLOBAL."""
    valid_domains = ["PROD", "FE", "BE", "DS", "UI", "GLOBAL"]
    if domain not in valid_domains:
        logger.warning(f"[DB WARN] Invalid domain rejected: {domain}")
        return False
        
    try:
        with get_connection() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO domain_constraints (domain, constraint_text, risk_level) VALUES (?, ?, ?)",
                (domain, text, risk)
            )
        return True
    except sqlite3.Error as e:
        logger.error(f"[DB ERROR] Update constraint failed: {e}")
        return False

def get_constraints() -> dict:
    """Retrieves all constraints currently in the database."""
    try:
        with get_connection() as conn:
            rows = conn.execute("SELECT domain, constraint_text, risk_level FROM domain_constraints").fetchall()
            return {r["domain"]: {"text": r["constraint_text"], "risk": r["risk_level"]} for r in rows}
    except sqlite3.Error as e:
        logger.error(f"[DB ERROR] Fetch constraints failed: {e}")
        return {}

def upsert_glossary_term(term: str, definition: str) -> bool:
    """Upserts a term into the project dictionary."""
    try:
        with get_connection() as conn:
            conn.execute("INSERT OR REPLACE INTO project_glossary (term, definition) VALUES (?, ?)", (term, definition))
        return True
    except sqlite3.Error as e:
        logger.error(f"[DB ERROR] Upsert glossary failed: {e}")
        return False

def get_glossary() -> dict:
    """Retrieves the full project dictionary."""
    try:
        with get_connection() as conn:
            rows = conn.execute("SELECT term, definition FROM project_glossary ORDER BY term ASC").fetchall()
            return {r["term"]: r["definition"] for r in rows}
    except sqlite3.Error as e:
        logger.error(f"[DB ERROR] Fetch glossary failed: {e}")
        return {}

def clear_ledger() -> bool:
    """Delete all rows from the chat ledger, domain constraints, and project glossary."""
    try:
        with get_connection() as conn:
            conn.execute("DELETE FROM chat_ledger")
            conn.execute("DELETE FROM domain_constraints")
            conn.execute("DELETE FROM project_glossary")
        return True
    except sqlite3.Error as e:
        logger.error(f"[DB ERROR] Clear ledger failed: {e}")
        return False

init_db()