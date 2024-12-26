import os
from datetime import timedelta
from urllib.parse import quote_plus

class Config:
    SECRET_KEY = os.urandom(32)
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    REMEMBER_COOKIE_DURATION = timedelta(days=1)

    USERNAME = 'shaya'
    PASSWORD = '@ShAyAcAfE0318@'
    PASSWORD = quote_plus(PASSWORD)
    HOST = 'localhost'
    DB = 'shayaDB'
    SQLALCHEMY_DATABASE_URI = f'mysql://{USERNAME}:{PASSWORD}@{HOST}/{DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
