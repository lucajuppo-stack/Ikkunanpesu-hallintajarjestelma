from flask import Flask
from db import close_db
from utils import utility_processor
from auth import init_auth_routes
from orders import init_order_routes

app = Flask(__name__)
app.secret_key = "super-salainen-avain"
app.teardown_appcontext(close_db)
app.context_processor(utility_processor)

init_auth_routes(app)
init_order_routes(app)
