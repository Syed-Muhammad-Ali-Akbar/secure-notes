import sqlite3
from backend.encryption import encrypt, decrypt

DB_FILE = "notes.db"

def init_db():
    """Initialize the SQLite database if it does not exist."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def save_note(title: str, content: str, key: bytes):
    """Encrypt and save a new note into the database."""
    enc_content = encrypt(content, key)
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, enc_content))
    conn.commit()
    conn.close()


def load_notes(key: bytes):
    """Load and decrypt all notes from the database."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, title, content FROM notes")
    rows = c.fetchall()
    conn.close()

    notes = []
    for r in rows:
        try:
            dec = decrypt(r[2], key)
            notes.append((r[0], r[1], dec))
        except Exception:
            notes.append((r[0], r[1], "[DECRYPTION FAILED]"))
    return notes


def get_note(note_id: int, key: bytes):
    """Retrieve a single note by ID."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, title, content FROM notes WHERE id=?", (note_id,))
    row = c.fetchone()
    conn.close()

    if row:
        try:
            dec = decrypt(row[2], key)
            return (row[0], row[1], dec)
        except Exception:
            return (row[0], row[1], "[DECRYPTION FAILED]")
    return None


def update_note(note_id: int, new_title: str, new_content: str, key: bytes):
    """Update an existing note with new encrypted content."""
    enc_content = encrypt(new_content, key)
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE notes SET title=?, content=? WHERE id=?", (new_title, enc_content, note_id))
    conn.commit()
    conn.close()


def delete_note(note_id: int):
    """Delete a note from the database by ID."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM notes WHERE id=?", (note_id,))
    conn.commit()
    conn.close()
