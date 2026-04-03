from flask import abort, request, session

STATUS_LABELS = {
    "pending": "Odottaa",
    "done": "Pesty",
    "invoiced": "Laskutettu",
    "paid": "Maksettu",
}


def status_label(status):
    return STATUS_LABELS.get(status, status)


def utility_processor():
    return {"status_label": status_label}


def check_csrf():
    form_token = request.form.get("csrf_token")
    if not form_token or form_token != session.get("csrf_token"):
        abort(403)


def get_order_categories(db, order_id):
    rows = db.execute(
        "SELECT c.name FROM categories c "
        "JOIN wash_order_categories woc ON c.id = woc.category_id "
        "WHERE woc.wash_order_id = ?",
        (order_id,)
    ).fetchall()
    return [row["name"] for row in rows]


def get_order_category_ids(db, order_id):
    rows = db.execute(
        "SELECT category_id FROM wash_order_categories WHERE wash_order_id = ?",
        (order_id,)
    ).fetchall()
    return [row["category_id"] for row in rows]
