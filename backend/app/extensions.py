"""Flask extension instances.

Extensions are instantiated here without binding to a specific app,
then initialized with the app in the factory function (create_app).
"""

from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
jwt = JWTManager()
cors = CORS()
