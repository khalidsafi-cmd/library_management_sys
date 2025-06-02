from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from app.routes import auth_routes, book_routes, checkout_routes
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(book_routes.bp)
    app.register_blueprint(checkout_routes.bp)

    return app
