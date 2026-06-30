from flask import Flask

from config import Config
from app.extensions import db, login_manager, migrate


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    login_manager.login_view = "auth.login"

    from app.models import User, Bus, Booking

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes.auth import auth
    from app.routes.admin import admin
    from app.routes.user import user

    app.register_blueprint(auth)
    app.register_blueprint(admin)
    app.register_blueprint(user)

    @app.route("/")
    def home():
        from flask import render_template
        return render_template("index.html")

    return app