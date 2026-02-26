from .database import get_db

def get_all_notes():
    db = get_db()
    return db.execute("SELECT * FROM notes ORDER BY id DESC").fetchall()

def create_note(title, content):
    db = get_db()
    db.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))
    db.commit()

def update_note(note_id, title, content):
    db = get_db()
    db.execute(
        "UPDATE notes SET title = ?, content = ? WHERE id = ?",
        (title, content, note_id)
    )
    db.commit()

def delete_note(note_id):
    db = get_db()
    db.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    db.commit()