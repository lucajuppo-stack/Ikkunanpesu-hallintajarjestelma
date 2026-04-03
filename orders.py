from flask import render_template, request, redirect, session
from db import get_db
from utils import check_csrf, get_order_categories


def init_order_routes(app):
    @app.route("/")
    def index():
        if "user_id" not in session:
            return render_template("index.html", orders=[])

        search_query = request.args.get("search", "")
        status_filter = request.args.get("status", "")
        db = get_db()

        query = (
            "SELECT wash_orders.*, users.username AS author "
            "FROM wash_orders "
            "LEFT JOIN users ON wash_orders.user_id = users.id"
        )
        params = []
        conditions = []

        if search_query:
            conditions.append("address LIKE ?")
            params.append("%" + search_query + "%")

        if status_filter and status_filter != "all":
            conditions.append("status = ?")
            params.append(status_filter)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY wash_date ASC"
        orders = db.execute(query, tuple(params)).fetchall()

        orders = [dict(order) for order in orders]
        for order in orders:
            order["categories"] = get_order_categories(db, order["id"])

        return render_template("index.html", orders=orders)

    @app.route("/new_order", methods=["GET", "POST"])
    def new_order():
        if "user_id" not in session:
            return redirect("/login")

        db = get_db()
        categories = db.execute("SELECT * FROM categories ORDER BY name").fetchall()

        if request.method == "POST":
            check_csrf()
            address = request.form["address"]
            price = request.form["price"]
            window_count = request.form["window_count"]
            wash_date = request.form["wash_date"]
            contact_info = request.form["contact_info"]
            user_id = session["user_id"]
            category_id = request.form.get("category")
            if category_id and category_id.isdigit():
                category_id = int(category_id)
            else:
                category_id = None

            cursor = db.execute(
                "INSERT INTO wash_orders (address, price, window_count, wash_date, contact_info, status, user_id, category_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (address, price, window_count, wash_date, contact_info, "pending", user_id, category_id)
            )
            order_id = cursor.lastrowid

            if category_id:
                db.execute(
                    "INSERT OR IGNORE INTO wash_order_categories (wash_order_id, category_id) VALUES (?, ?)",
                    (order_id, category_id)
                )

            db.commit()
            return redirect("/")

        return render_template("new_order.html", categories=categories, selected_categories=[])

    @app.route("/edit/<int:id>", methods=["GET", "POST"])
    def edit_order(id):
        if "user_id" not in session:
            return redirect("/login")

        db = get_db()
        order = db.execute("SELECT * FROM wash_orders WHERE id = ?", (id,)).fetchone()
        if not order or order["user_id"] != session["user_id"]:
            return redirect("/")

        categories = db.execute("SELECT * FROM categories ORDER BY name").fetchall()

        if request.method == "POST":
            check_csrf()
            address = request.form["address"]
            price = request.form["price"]
            window_count = request.form["window_count"]
            wash_date = request.form["wash_date"]
            contact_info = request.form["contact_info"]
            status = request.form["status"]
            category_id = request.form.get("category")
            if category_id and category_id.isdigit():
                category_id = int(category_id)
            else:
                category_id = None

            db.execute(
                "UPDATE wash_orders SET address=?, price=?, window_count=?, wash_date=?, contact_info=?, status=?, category_id=? WHERE id=?",
                (address, price, window_count, wash_date, contact_info, status, category_id, id)
            )
            db.execute("DELETE FROM wash_order_categories WHERE wash_order_id = ?", (id,))

            if category_id:
                db.execute(
                    "INSERT OR IGNORE INTO wash_order_categories (wash_order_id, category_id) VALUES (?, ?)",
                    (id, category_id)
                )

            db.commit()
            return redirect("/")

        selected_categories = [order["category_id"]] if order["category_id"] else []
        return render_template("edit_order.html", order=order, categories=categories, selected_categories=selected_categories)

    @app.route("/order/<int:id>", methods=["GET", "POST"])
    def order_detail(id):
        db = get_db()
        order = db.execute(
            "SELECT wash_orders.*, users.username AS author FROM wash_orders "
            "JOIN users ON wash_orders.user_id = users.id "
            "WHERE wash_orders.id = ?",
            (id,)
        ).fetchone()

        if not order:
            return redirect("/")

        categories = get_order_categories(db, id)
        comments = db.execute(
            "SELECT oc.comment_text, oc.created_at, u.username FROM order_comments oc "
            "JOIN users u ON oc.user_id = u.id "
            "WHERE oc.wash_order_id = ? ORDER BY oc.created_at ASC",
            (id,)
        ).fetchall()
        error = None

        if request.method == "POST":
            if "user_id" not in session:
                return redirect("/login")

            check_csrf()
            if session["user_id"] == order["user_id"]:
                error = "Et voi kommentoida omaa tilaustasi."
            else:
                comment_text = request.form["comment_text"].strip()
                if not comment_text:
                    error = "Kirjoita kommentti ennen lähettämistä."
                else:
                    db.execute(
                        "INSERT INTO order_comments (wash_order_id, user_id, comment_text) VALUES (?, ?, ?)",
                        (id, session["user_id"], comment_text)
                    )
                    db.commit()
                    return redirect(f"/order/{id}")

        return render_template("order_detail.html", order=order, categories=categories, comments=comments, error=error)

    @app.route("/profile")
    def profile():
        if "user_id" not in session:
            return redirect("/login")
        return redirect(f"/user/{session['username']}")

    @app.route("/user/<username>")
    def user_profile(username):
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if not user:
            return redirect("/")

        orders = db.execute(
            "SELECT * FROM wash_orders WHERE user_id = ? ORDER BY wash_date ASC",
            (user["id"],)
        ).fetchall()
        orders = [dict(order) for order in orders]
        for order in orders:
            order["categories"] = get_order_categories(db, order["id"])

        stats = db.execute(
            "SELECT status, COUNT(*) AS count FROM wash_orders WHERE user_id = ? GROUP BY status",
            (user["id"],)
        ).fetchall()

        summary = db.execute(
            "SELECT COUNT(*) AS total_orders, COALESCE(SUM(price), 0) AS total_price FROM wash_orders WHERE user_id = ?",
            (user["id"],)
        ).fetchone()

        category_stats = db.execute(
            "SELECT c.name, COUNT(*) AS count FROM categories c "
            "JOIN wash_order_categories woc ON c.id = woc.category_id "
            "JOIN wash_orders wo ON wo.id = woc.wash_order_id "
            "WHERE wo.user_id = ? GROUP BY c.name",
            (user["id"],)
        ).fetchall()

        return render_template(
            "user_profile.html",
            user=user,
            orders=orders,
            stats=stats,
            summary=summary,
            category_stats=category_stats,
        )

    @app.route("/delete/<int:id>", methods=["POST"])
    def delete_order(id):
        if "user_id" not in session:
            return redirect("/login")

        check_csrf()
        db = get_db()
        order = db.execute("SELECT * FROM wash_orders WHERE id = ?", (id,)).fetchone()
        if not order or order["user_id"] != session["user_id"]:
            return redirect("/")

        db.execute("DELETE FROM wash_orders WHERE id = ?", (id,))
        db.execute("DELETE FROM wash_order_categories WHERE wash_order_id = ?", (id,))
        db.execute("DELETE FROM order_comments WHERE wash_order_id = ?", (id,))
        db.commit()
        return redirect("/")
