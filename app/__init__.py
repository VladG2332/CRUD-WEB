from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    # Importar y registrar las rutas
    from .routes import estudiantes_bp
    app.register_blueprint(estudiantes_bp)

    # Crear tablas en la base de datos
    with app.app_context():
        db.create_all()

    return app