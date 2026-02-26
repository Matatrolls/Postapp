from flask import Blueprint, render_template, request, redirect, url_for
from .models import get_all_notes, create_note, update_note, delete_note

main = Blueprint("main", __name__)

@main.route("/")
def index():
    notes = get_all_notes()
    return render_template("index.html", notes=notes)

@main.route("/create", methods=["POST"])
def create():
    create_note(request.form["title"], request.form["content"])
    return redirect(url_for("main.index"))

@main.route("/edit/<int:note_id>", methods=["POST"])
def edit(note_id):
    update_note(note_id, request.form["title"], request.form["content"])
    return redirect(url_for("main.index"))

@main.route("/delete/<int:note_id>", methods=["POST"])
def delete(note_id):
    delete_note(note_id)
    return redirect(url_for("main.index"))