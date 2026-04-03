import secrets
from flask import render_template, request, redirect, session, abort
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db
from utils import check_csrf


def init_auth_routes(app):
    @app.before_request
    def ensure_csrf_token():
        if "user_id" in session and "csrf_token" not in session:
            session["csrf_token"] = secrets.token_hex(16)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            db = get_db()
            user = db.execute(
                "SELECT * FROM users WHERE username = ?",
                (username,)
            ).fetchone()

            if user and check_password_hash(user["password"], password):
                session["user_id"] = user["id"]
                session["username"] = user["username"]
                session["csrf_token"] = secrets.token_hex(16)
                return redirect("/")
            return render_template("login.html", error="Väärä käyttäjätunnus tai salasana.")

        return render_template("login.html")

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            password_hash = generate_password_hash(password)
            db = get_db()
            try:
                db.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (username, password_hash)
                )
                db.commit()
                return redirect("/")
            except Exception:
                return render_template("register.html", error="Käyttäjätunnus on jo varattu.")

        return render_template("register.html")

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect("/")
