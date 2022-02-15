
from flask import Flask
import os
from src.auth import auth
from src.students import student
from src.registration import registration
from src.charges import charges
from src.period import period
from src.admin import admin
from src.wallet import wallet
from src.database import db
from flask_cors import CORS
from flask_jwt_extended import JWTManager


def create_app(test_config=None):
    app = Flask(__name__,instance_relative_config=True)
    CORS(app)

    my_env = os.getenv("FLASK_ENV")
    if(my_env=="development"):
        uri = "postgresql://postgres:Foluke89@localhost/jets"
    else:
        uri = os.getenv("DATABASE_URL")
        if uri.startswith("postgres://"):
            uri = uri.replace("postgres://", "postgresql://", 1)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY = os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI = uri,
            SQLALCHEMY_TRACK_MODIFICATIONS = False,
            JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY"),
        )
    else:
        app.config.from_mapping(test_config)
    

    @app.get("/")
    def hello():
        return {"Hello":"This was authored by Moses Bamidele"}

    db.app=app
    db.init_app(app)

    JWTManager(app)

    app.register_blueprint(auth)
    app.register_blueprint(student)
    app.register_blueprint(registration)
    app.register_blueprint(charges)
    app.register_blueprint(period)
    app.register_blueprint(admin)
    app.register_blueprint(wallet)

    return app