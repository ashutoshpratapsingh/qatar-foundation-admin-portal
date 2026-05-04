import os
from datetime import timedelta

class Config:
    SECRET_KEY = "supersecretkey"
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite3"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = "jwt-secret"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)