import sqlite3
import logging
from pathlib import Path

logger = logging.getLogger("naur.state")
BASE_DIR = Path(__file__).parent.parent
DB_FILE = BASE_DIR / "naur_state.db"


def get_connection() -> sqlite3.Connection:
    """Open and return a SQLite connection to the application database.

    Returns:
        A ``sqlite3.Connection`` with ``row_factory`` set to ``sqlite3.Row``
        so columns are accessible by name.
    """
    conn = sqlite3.connect(DB_FILE, check_same_thread=False, timeout=15.0)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create all required database tables if they do not already exist.

    Creates three tables: ``chat_ledger``, ``domain_constraints``, and
    ``project_glossary``.  Safe to call on every startup (idempotent).
    """
    with get_connection() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS chat_ledger "
            "(id INTEGER PRIMARY KEY AUTOINCREMENT, role TEXT, content TEXT)"
        )
        conn.execute(
            "CREATE TABLE IF NOT EXISTS domain_constraints "
            "(domain TEXT PRIMARY KEY, constraint_text TEXT, business_impact TEXT, deep_dive TEXT, risk_level TEXT)"
        )
        conn.execute(
            "CREATE TABLE IF NOT EXISTS project_glossary (term TEXT PRIMARY KEY, definition TEXT)"
        )


def append_message(role: str, content: str) -> bool:
    """Append a chat message to the ledger.

    Args:
        role: Speaker role identifier, e.g. ``"human"`` or ``"assistant"``.
        content: Full message text to persist.

    Returns:
        ``True`` on success, ``False`` if a database error occurs.
    """
    try:
        with get_connection() as conn:
            conn.execute("INSERT INTO chat_ledger (role, content) VALUES (?, ?)", (role, content))
        return True
    except sqlite3.Error:
        return False


def get_chat_history() -> list[dict]:
    """Retrieve the full chat history in insertion order.

    Returns:
        A list of ``{"role": str, "content": str}`` dicts, oldest first.
        Returns an empty list on error.
    """
    try:
        with get_connection() as conn:
            rows = conn.execute("SELECT role, content FROM chat_ledger ORDER BY id ASC").fetchall()
            return [{"role": r["role"], "content": r["content"]} for r in rows]
    except sqlite3.Error:
        return []


def update_constraint(domain: str, text: str, business_impact: str, deep_dive: str, risk: str) -> bool:
    """Insert or replace a domain constraint record.

    Args:
        domain: One of ``PROD``, ``FE``, ``BE``, ``DS``, ``UI``, ``GLOBAL``.
        text: Technical constraint description.
        business_impact: Plain-language business impact statement.
        deep_dive: Long-form technical explanation.
        risk: Risk level — ``HIGH``, ``MEDIUM``, or ``LOW``.

    Returns:
        ``True`` on success, ``False`` if the domain is invalid or a
        database error occurs.
    """
    valid_domains = ["PROD", "FE", "BE", "DS", "UI", "GLOBAL"]
    if domain not in valid_domains:
        return False
    try:
        with get_connection() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO domain_constraints "
                "(domain, constraint_text, business_impact, deep_dive, risk_level) VALUES (?, ?, ?, ?, ?)",
                (domain, text, business_impact, deep_dive, risk),
            )
        return True
    except sqlite3.Error:
        return False


def get_constraints() -> dict:
    """Fetch all domain constraints as a keyed dictionary.

    Returns:
        A dict mapping domain keys to constraint payload dicts with keys
        ``text``, ``business``, ``deep_dive``, and ``risk``.
        Returns an empty dict on error.
    """
    try:
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT domain, constraint_text, business_impact, deep_dive, risk_level FROM domain_constraints"
            ).fetchall()
            return {
                r["domain"]: {
                    "text": r["constraint_text"],
                    "business": r["business_impact"],
                    "deep_dive": r["deep_dive"],
                    "risk": r["risk_level"],
                }
                for r in rows
            }
    except sqlite3.Error:
        return {}


def upsert_glossary_term(term: str, defn: str) -> bool:
    """Insert or replace a term in the project glossary.

    Args:
        term: The glossary term (used as the primary key).
        defn: The plain-language definition for the term.

    Returns:
        ``True`` on success, ``False`` if a database error occurs.
    """
    try:
        with get_connection() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO project_glossary (term, definition) VALUES (?, ?)", (term, defn)
            )
        return True
    except sqlite3.Error:
        return False


def get_glossary() -> dict:
    """Retrieve all glossary terms sorted alphabetically.

    Returns:
        A dict mapping term strings to their definition strings.
        Returns an empty dict on error.
    """
    try:
        with get_connection() as conn:
            rows = conn.execute("SELECT term, definition FROM project_glossary ORDER BY term ASC").fetchall()
            return {r["term"]: r["definition"] for r in rows}
    except sqlite3.Error:
        return {}


def clear_ledger() -> bool:
    """Delete all rows from every application table.

    Clears ``chat_ledger``, ``domain_constraints``, and ``project_glossary``
    in a single transaction.

    Returns:
        ``True`` on success, ``False`` if a database error occurs.
    """
    try:
        with get_connection() as conn:
            conn.execute("DELETE FROM chat_ledger")
            conn.execute("DELETE FROM domain_constraints")
            conn.execute("DELETE FROM project_glossary")
        return True
    except sqlite3.Error:
        return False


init_db()
