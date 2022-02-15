from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)

db = SQLAlchemy(session_options={"autoflush": False})
migrate = Migrate()
marshmallow = Marshmallow()
cors = CORS()


@app.errorhandler(404)
def _404(e):
    return jsonify(msg="not found"), 404


def run():
    """flask app factory"""

    from .config import Config

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    marshmallow.init_app(app)
    cors.init_app(app)

    from .controller import post, admin, auth, api
    from .utils.filter import _filter

    app.register_blueprint(post)
    app.register_blueprint(admin)
    app.register_blueprint(auth)
    app.register_blueprint(_filter)
    app.register_blueprint(api, url_prefix="/api/v1")

    from .model import Admin

    # login manager
    login_manager = LoginManager()
    login_manager.login_view = "auth.Login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return Admin.query.get(int(id))

    return app
