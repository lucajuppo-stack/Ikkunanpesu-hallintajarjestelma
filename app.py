from flask import Flask, render_template, request, redirect, session
from db import get_db, close_db

app = Flask(__name__)
app.secret_key = "super-salainen-avain"
app.teardown_appcontext(close_db)

@app.route("/")
def index():
    if "user_id" not in session:
        return render_template("index.html", orders=[])

    search_query = request.args.get("search", "")
    db = get_db()
    
    if search_query:
        query = "SELECT * FROM wash_orders WHERE address LIKE ? ORDER BY wash_date ASC"
        orders = db.execute(query, ("%" + search_query + "%",)).fetchall()
    else:
        orders = db.execute("SELECT * FROM wash_orders ORDER BY wash_date ASC").fetchall()
    
    return render_template("index.html", orders=orders)

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

        if user and user["password"] == password:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect("/")
        else:
            return render_template("login.html", error="Väärä käyttäjätunnus tai salasana.")

    return render_template("login.html")

@app.route("/new_order", methods=["GET", "POST"])
def new_order():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        address = request.form["address"]
        price = request.form["price"]
        window_count = request.form["window_count"]
        wash_date = request.form["wash_date"]
        contact_info = request.form["contact_info"]
        user_id = session["user_id"]
        
        db = get_db()
        db.execute(
            "INSERT INTO wash_orders (address, price, window_count, wash_date, contact_info, status, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (address, price, window_count, wash_date, contact_info, "pending", user_id)
        )
        db.commit()
        return redirect("/")

    return render_template("new_order.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        
        try:
            db.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            db.commit()
            return redirect("/") 
        except:
            return render_template("register.html", error="Käyttäjätunnus on jo varattu.")
            
    return render_template("register.html")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_order(id):
    if "user_id" not in session:
        return redirect("/login")
        
    db = get_db()
    
    if request.method == "POST":
        address = request.form["address"]
        price = request.form["price"]
        window_count = request.form["window_count"]
        wash_date = request.form["wash_date"]
        contact_info = request.form["contact_info"]
        status = request.form["status"]
        
        db.execute(
            "UPDATE wash_orders SET address=?, price=?, window_count=?, wash_date=?, contact_info=?, status=? WHERE id=?",
            (address, price, window_count, wash_date, contact_info, status, id)
        )
        db.commit()
        return redirect("/")
    
    order = db.execute("SELECT * FROM wash_orders WHERE id = ?", (id,)).fetchone()
    return render_template("edit_order.html", order=order)

@app.route("/delete/<int:id>", methods=["POST"])
def delete_order(id):
    if "user_id" not in session:
        return redirect("/login")
        
    db = get_db()
    db.execute("DELETE FROM wash_orders WHERE id = ?", (id,))
    db.commit()
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")