from flask import Flask

# Import the Config class that we created in the config.py file
from config import Config

# Import the 'site' blueprint that we created in routes.py
from .site.routes import site;

from .authentication.routes import auth
from .api.routes import api

from flask_migrate import Migrate
from .models import db as root_db, login_manager, ma

from flask_cors import CORS

from .helpers import JSONEncoder

# Create an instance of the class
app = Flask(__name__)

app.config.from_object(Config)

# Register the application/blueprint
app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(api)

root_db.init_app(app)
migrate = Migrate(app, root_db)

login_manager.init_app(app)
login_manager.login_view = 'auth.signin' # specify what page to load for NON-AUTHED users

ma.init_app(app)

CORS(app)

app.json_encoder = JSONEncoder

from.car_inventory import models