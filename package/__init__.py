from flask import Flask, request
from flask_migrate import Migrate

from package.azure_database import Base, Session, engine

# Config + Blueprints
from package.configurations.config import config_by_name
from package.routes import home_bp
from package.routes.car_routes import car_bp
from package.routes.product_routes import product_bp
from package.routes.user_routes import user_bp

# Utils
from package.utils.error_handlers import register_error_handlers
from package.utils.logging_middleware import setup_logging_middleware

migrate = Migrate()


def create_app(config_name="dev"):
    app = Flask(__name__)

    # Load config
    app.config.from_object(config_by_name[config_name])

    # Setup DB + migrations
    Base.metadata.create_all(bind=engine)
    migrate.init_app(app, Base)

    # Register blueprints
    app.register_blueprint(home_bp, url_prefix="/home")
    app.register_blueprint(user_bp, url_prefix="/users")
    app.register_blueprint(product_bp, url_prefix="/products")
    app.register_blueprint(car_bp, url_prefix="/cars")

    # Middlewares
    setup_logging_middleware(app)

    # Error handling
    register_error_handlers(app)

    # SQLAlchemy session handling per request
    @app.before_request
    def create_session():
        request.db_session = Session()

    @app.teardown_request
    def remove_session(exception=None):
        db_session = getattr(request, "db_session", None)
        if db_session:
            if exception:
                db_session.rollback()
            else:
                db_session.commit()
            db_session.close()
            Session.remove()

    return app
