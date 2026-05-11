import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Please login first."

def create_app():
    app = Flask(__name__)

    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    db_path = os.path.join(base_dir, "database", "assets.db")

    app.config["SECRET_KEY"] = "change-this-secret-key-later"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path.replace("\\", "/")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    login_manager.init_app(app)

    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes.main import main
    from app.auth.routes import auth

    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app
