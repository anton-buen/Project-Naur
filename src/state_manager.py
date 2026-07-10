import sqlite3
import logging
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_FILE = os.path.join(BASE_DIR, "naur_state.db")

logger = logging.getLogger("naur.state_manager")

def get_connection():
    """Return a WAL-mode SQLite connection with a 10-second busy timeout."""
    conn = sqlite3.connect(DB_FILE, timeout=10.0)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Create all required tables if they do not already exist."""
    try:
        with get_connection() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS chat_ledger (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                );
                
                CREATE TABLE IF NOT EXISTS domain_constraints (
                    domain TEXT PRIMARY KEY,
                    constraint_text TEXT NOT NULL,
                    risk_level TEXT,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                );
                
                CREATE TABLE IF NOT EXISTS project_glossary (
                    term TEXT PRIMARY KEY,
                    definition TEXT NOT NULL,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                );
            """)
        logger.info("[DB INIT] SQLite database initialized successfully in WAL mode.")
    except sqlite3.Error as e:
        logger.error(f"[DB ERROR] Failed to initialize database: {e}")

def append_message(role: str, content: str) -> bool:
    """Insert a message into the chat ledger. Returns True on success."""
    try:
        with get_connection() as conn:
            conn.execute("INSERT INTO chat_ledger (role, content) VALUES (?, ?)", (role, content))
        return True
    except sqlite3.Error as e:
        logger.error(f"[DB ERROR] Append message failed: {e}")
        return False

def get_chat_history() -> list:
    """Return all chat ledger rows ordered by insertion sequence."""
    try:
        with get_connection() as conn:
            rows = conn.execute("SELECT role, content FROM chat_ledger ORDER BY id ASC").fetchall()
            return [{"role": r["role"], "content": r["content"]} for r in rows]
    except sqlite3.Error as e:
        logger.error(f"[DB ERROR] Get chat history failed: {e}")
        return []

def clear_ledger() -> bool:
    """Delete all rows from the chat ledger. Domain constraints and glossary are preserved."""
    try:
        with get_connection() as conn:
            conn.execute("DELETE FROM chat_ledger")
            #conn.execute("DELETE FROM domain_constraints")
        return True
    except sqlite3.Error as e:
        logger.error(f"[DB ERROR] Clear ledger failed: {e}")
        return False

def update_constraint(domain: str, constraint_text: str, risk_level: str = "LOW") -> bool:
    """Upsert a domain constraint record. Returns True on success."""
    try:
        with get_connection() as conn:
            conn.execute("""
                INSERT INTO domain_constraints (domain, constraint_text, risk_level) 
                VALUES (?, ?, ?)
                ON CONFLICT(domain) DO UPDATE SET 
                    constraint_text=excluded.constraint_text,
                    risk_level=excluded.risk_level,
                    updated_at=CURRENT_TIMESTAMP;
            """, (domain, constraint_text, risk_level))
        return True
    except sqlite3.Error as e:
        logger.error(f"[DB ERROR] Update constraint failed: {e}")
        return False

def get_constraints() -> dict:
    """Return all domain constraints keyed by domain name."""
    try:
        with get_connection() as conn:
            rows = conn.execute("SELECT domain, constraint_text, risk_level FROM domain_constraints").fetchall()
            return {r["domain"]: {"text": r["constraint_text"], "risk": r["risk_level"]} for r in rows}
    except sqlite3.Error as e:
        logger.error(f"[DB ERROR] Get constraints failed: {e}")
        return {}

def upsert_glossary_term(term: str, definition: str) -> bool:
    """Insert or update a glossary term. Returns True on success."""
    try:
        with get_connection() as conn:
            conn.execute("""
                INSERT INTO project_glossary (term, definition) 
                VALUES (?, ?)
                ON CONFLICT(term) DO UPDATE SET 
                    definition=excluded.definition,
                    updated_at=CURRENT_TIMESTAMP;
            """, (term, definition))
        return True
    except sqlite3.Error as e:
        logger.error(f"[DB ERROR] Upsert glossary failed: {e}")
        return False

def get_glossary() -> dict:
    """Return all glossary terms keyed by term name."""
    try:
        with get_connection() as conn:
            rows = conn.execute("SELECT term, definition FROM project_glossary").fetchall()
            return {r["term"]: r["definition"] for r in rows}
    except sqlite3.Error as e:
        logger.error(f"[DB ERROR] Get glossary failed: {e}")
        return {}

init_db()

