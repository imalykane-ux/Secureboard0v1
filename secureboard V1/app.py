import os
import json
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-later")

ADMIN_USER = os.environ.get("ADMIN_USER", "codexcapital")
ADMIN_PASS = os.environ.get("ADMIN_PASS", "Testing123")

LOG_FILE = "logs.json"


def load_logs():
    if not os.path.exists(LOG_FILE):
        return []

    try:
        with open(LOG_FILE, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []


def save_logs(logs):
    with open(LOG_FILE, "w") as file:
        json.dump(logs, file, indent=4)


def login_required(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        if not session.get("admin_logged_in"):
            flash("Please log in first.", "error")
            return redirect(url_for("admin_login"))
        return route_function(*args, **kwargs)

    return wrapper


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form.get("username", "Anonymous").strip()
        message = request.form.get("message", "").strip()
        ip_address = request.remote_addr or "unknown"

        if not username:
            username = "Anonymous"

        if not message:
            flash("Message cannot be empty.", "error")
            return redirect(url_for("index"))

        logs = load_logs()

        new_log = {
            "id": len(logs) + 1,
            "username": username,
            "message": message,
            "ip_address": ip_address,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        logs.append(new_log)
        save_logs(logs)

        flash("Message posted successfully.", "success")
        return redirect(url_for("index"))

    logs = load_logs()
    logs = sorted(logs, key=lambda log: log.get("timestamp", ""), reverse=True)

    return render_template("index.html", logs=logs)


@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if username == ADMIN_USER and password == ADMIN_PASS:
            session["admin_logged_in"] = True
            flash("Admin login successful.", "success")
            return redirect(url_for("admin"))

        flash("Invalid admin username or password.", "error")

    return render_template("admin_login.html")


@app.route("/admin/logs")
@login_required
def admin():
    logs = load_logs()
    logs = sorted(logs, key=lambda log: log.get("timestamp", ""), reverse=True)

    return render_template("admin.html", logs=logs)


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for("admin_login"))


if __name__ == "__main__":
    app.run(debug=True)
