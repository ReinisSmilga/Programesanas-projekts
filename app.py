from flask import Flask, render_template, request, redirect
import sqlite3
from pathlib import Path

app = Flask(__name__)

def get_db_connection():
    db = Path(__file__).parent / "events.db"
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/pasakumi")
def events():
    events = get_events()
    return render_template("events.html", events=events)

@app.route("/pasakumi/<int:event_id>")
def event_detail(event_id):
    event = get_events("WHERE events.id = ?", (event_id,))[0]
    return render_template("event_bio.html", event=event)

@app.route("/par-mums")
def about():
    return render_template("about.html")

@app.route("/palidzibas")
def help_page():
    return render_template("help.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

def get_events(where_clause="", params=()):
    conn = get_db_connection()

    events = conn.execute(f"""
        SELECT 
            events.id,
            events.title,
            events.event_date,
            events.description,
            locations.name AS location,
            locations.address AS address,
            organizers.name AS organizer,
            categories.category_name,
            categories.subcategory_name
        FROM events
        JOIN locations ON events.location_id = locations.id
        JOIN organizers ON events.organizer_id = organizers.id
        JOIN categories ON events.category_id = categories.id
        {where_clause}
        ORDER BY events.event_date
    """, params).fetchall()

    conn.close()
    return events

@app.route("/pasakumi/<int:event_id>/edit", methods=["GET", "POST"])
def edit_event(event_id):
    conn = get_db_connection()

    event = conn.execute("SELECT * FROM events WHERE id = ?", (event_id,)).fetchone()
    locations = conn.execute("SELECT * FROM locations").fetchall()
    organizers = conn.execute("SELECT * FROM organizers").fetchall()
    categories = conn.execute("SELECT * FROM categories").fetchall()

    if request.method == "POST":
        conn.execute("""
            UPDATE events
            SET title = ?, event_date = ?, location_id = ?, organizer_id = ?, category_id = ?, description = ?
            WHERE id = ?
        """, (
            request.form["title"],
            request.form["event_date"],
            request.form["location_id"],
            request.form["organizer_id"],
            request.form["category_id"],
            request.form["description"],
            event_id
        ))

        conn.commit()
        conn.close()

        return redirect("/pasakumi")

    conn.close()

    return render_template("edit.html", event=event, locations=locations, organizers=organizers, categories=categories)


@app.route("/pasakumi/<int:event_id>/delete", methods=["POST"])
def delete_event(event_id):
    conn = get_db_connection()

    conn.execute("DELETE FROM events WHERE id = ?", (event_id,))
    conn.commit()
    conn.close()

    return redirect("/pasakumi")

@app.route("/pasakumi/new/edit", methods=["GET", "POST"])
def add_event():
    conn = get_db_connection()

    locations = conn.execute("SELECT * FROM locations").fetchall()
    organizers = conn.execute("SELECT * FROM organizers").fetchall()
    categories = conn.execute("SELECT * FROM categories").fetchall()

    if request.method == "POST":
        conn.execute("""
            INSERT INTO events (title, event_date, location_id, organizer_id, category_id, description)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            request.form["title"],
            request.form["event_date"],
            request.form["location_id"],
            request.form["organizer_id"],
            request.form["category_id"],
            request.form["description"]
        ))

        conn.commit()
        conn.close()
        return redirect("/pasakumi")

    event = {
        "title": "",
        "event_date": "",
        "location_id": "",
        "organizer_id": "",
        "category_id": "",
        "description": ""
    }

    conn.close()

    return render_template("edit.html", event=event, locations=locations, organizers=organizers, categories=categories)

if __name__ == "__main__":
    app.run(debug=True)