from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/pasakumi")
def events():
    return render_template("events.html")

@app.route("/par-mums")
def about():
    return render_template("about.html")

@app.route("/palidzibas")
def help_page():
    return render_template("help.html")

if __name__ == "__main__":
    app.run(debug=True)