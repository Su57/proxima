from flask import Blueprint

from src.apps.common.routers.auth import bp as auth_bp
from src.apps.common.routers.file import bp as file_bp

common_bp = Blueprint("common", __name__)
common_bp.register_blueprint(auth_bp)
common_bp.register_blueprint(file_bp)
