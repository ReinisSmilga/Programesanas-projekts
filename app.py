from flask import Flask, render_template
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
    conn = get_db_connection()

    events = conn.execute("""
        SELECT 
            events.id,
            events.title,
            events.event_date,
            events.description,
            locations.name AS location,
            organizers.name AS organizer,
            categories.category_name,
            categories.subcategory_name
        FROM events
        JOIN locations ON events.location_id = locations.id
        JOIN organizers ON events.organizer_id = organizers.id
        JOIN categories ON events.category_id = categories.id
        ORDER BY events.event_date
    """).fetchall()

    conn.close()

    return render_template("events.html", events=events)

@app.route("/par-mums")
def about():
    return render_template("about.html")

@app.route("/palidzibas")
def help_page():
    return render_template("help.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)