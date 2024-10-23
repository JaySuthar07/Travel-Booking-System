from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  

# Create Flask app instance
app = Flask(__name__)

# Configure database URI and secret key
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///travelDB.db"
app.secret_key = 'your_secret_key_here'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'travel.login'   # Redirect unauthorized users to login page  

db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate with app and db

# Push application context
app.app_context().push()

from Travel.models import *


def create_app():
    # Register the blueprint
    from Travel.views import bp
    app.register_blueprint(bp)
    return app


# Create an instance of the app
