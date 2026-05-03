import os
from flask import Flask
from dotenv import load_dotenv
from db import close_db
from utils import utility_processor
from auth import init_auth_routes
from orders import init_order_routes

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-key-for-testing')
app.teardown_appcontext(close_db)
app.context_processor(utility_processor)

init_auth_routes(app)
init_order_routes(app)
