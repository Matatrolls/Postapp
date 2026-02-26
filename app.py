from flask import Flask, request, redirect, url_for, render_template_string
import sqlite3
import os

app = Flask(__name__)
DB_NAME = "notes.db"

# =========================
# DATABASE SETUP
# =========================
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# =========================
# HTML TEMPLATE
# =========================
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Notes Manager</title>
    <style>
        body { font-family: Arial; max-width: 700px; margin: auto; padding: 20px; }
        .note { border: 1px solid #ccc; padding: 10px; margin: 10px 0; }
        .actions { margin-top: 10px; }
        input, textarea { width: 100%; padding: 5px; margin: 5px 0; }
        button { padding: 5px 10px; }
    </style>
</head>
<body>

<h1>Notes Manager</h1>

<h2>Create Note</h2>
<form method="POST" action="/create">
    <input type="text" name="title" placeholder="Title" required>
    <textarea name="content" placeholder="Content" required></textarea>
    <button type="submit">Add Note</button>
</form>

<hr>

<h2>All Notes</h2>
{% for note in notes %}
<div class="note">
    <form method="POST" action="/edit/{{note[0]}}">
        <input type="text" name="title" value="{{note[1]}}" required>
        <textarea name="content" required>{{note[2]}}</textarea>
        <div class="actions">
            <button type="submit">Update</button>
        </div>
    </form>

    <form method="POST" action="/delete/{{note[0]}}" style="margin-top:5px;">
        <button type="submit" style="background:red;color:white;">Delete</button>
    </form>
</div>
{% else %}
<p>No notes yet.</p>
{% endfor %}

</body>
</html>
"""

# =========================
# ROUTES
# =========================
@app.route("/")
def index():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes")
    notes = cursor.fetchall()
    conn.close()
    return render_template_string(HTML, notes=notes)

@app.route("/create", methods=["POST"])
def create_note():
    title = request.form["title"]
    content = request.form["content"]

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))
    conn.commit()
    conn.close()

    return redirect(url_for("index"))

@app.route("/edit/<int:note_id>", methods=["POST"])
def edit_note(note_id):
    title = request.form["title"]
    content = request.form["content"]

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE notes SET title = ?, content = ? WHERE id = ?", 
                   (title, content, note_id))
    conn.commit()
    conn.close()

    return redirect(url_for("index"))

@app.route("/delete/<int:note_id>", methods=["POST"])
def delete_note(note_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("index"))

# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True)