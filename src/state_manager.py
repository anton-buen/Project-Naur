import sqlite3
import logging
import os

# 1. Dynamically find the absolute path to the root 'Project Naur' folder
# (Since this file is in src/, we go up one directory)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 2. Hardcode the absolute path to ensure all processes hit the exact same file
DB_FILE = os.path.join(BASE_DIR, "naur_state.db")

logger = logging.getLogger("naur.state_manager")

def get_connection():
    """Creates a database connection with WAL mode and timeout for concurrency."""
    # A 10-second timeout ensures UI reads don't fail immediately if Bob is writing
    conn = sqlite3.connect(DB_FILE, timeout=10.0)
    
    # [CRITICAL] Enable WAL/Write-Ahead Logging for concurrent reads/writes
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.row_factory = sqlite3.Row  # Return dict-like rows for easy JSON serialization
    return conn

def init_db():
    """Initializes the database schema if it doesn't exist."""
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

# --- Chat Ledger Functions ---
def append_message(role: str, content: str) -> bool:
    try:
        with get_connection() as conn:
            conn.execute("INSERT INTO chat_ledger (role, content) VALUES (?, ?)", (role, content))
        return True
    except sqlite3.Error as e:
        logger.error(f"[DB ERROR] Append message failed: {e}")
        return False

def get_chat_history() -> list:
    try:
        with get_connection() as conn:
            rows = conn.execute("SELECT role, content FROM chat_ledger ORDER BY id ASC").fetchall()
            return [{"role": r["role"], "content": r["content"]} for r in rows]
    except sqlite3.Error as e:
        logger.error(f"[DB ERROR] Get chat history failed: {e}")
        return []

def clear_ledger() -> bool:
    """Wipes the active session state (Used by the UI Reset Button)"""
    try:
        with get_connection() as conn:
            conn.execute("DELETE FROM chat_ledger")
            conn.execute("DELETE FROM domain_constraints")
            # We explicitly leave project_glossary intact so teams don't lose their shared dictionary!
        return True
    except sqlite3.Error as e:
        logger.error(f"[DB ERROR] Clear ledger failed: {e}")
        return False

# --- Domain Constraints Functions ---
def update_constraint(domain: str, constraint_text: str, risk_level: str = "LOW") -> bool:
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
    try:
        with get_connection() as conn:
            rows = conn.execute("SELECT domain, constraint_text, risk_level FROM domain_constraints").fetchall()
            return {r["domain"]: {"text": r["constraint_text"], "risk": r["risk_level"]} for r in rows}
    except sqlite3.Error as e:
        logger.error(f"[DB ERROR] Get constraints failed: {e}")
        return {}

# --- Glossary Functions ---
def upsert_glossary_term(term: str, definition: str) -> bool:
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
    try:
        with get_connection() as conn:
            rows = conn.execute("SELECT term, definition FROM project_glossary").fetchall()
            return {r["term"]: r["definition"] for r in rows}
    except sqlite3.Error as e:
        logger.error(f"[DB ERROR] Get glossary failed: {e}")
        return {}

# Initialize the database file automatically upon import
init_db()

