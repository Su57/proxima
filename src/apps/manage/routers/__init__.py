from flask import Blueprint

from src.apps.manage.routers.role import bp as role_bp
from src.apps.manage.routers.user import bp as user_bp
from src.apps.manage.routers.authority import bp as authority_bp

auth_bp = Blueprint("manage", __name__, url_prefix="/")
auth_bp.register_blueprint(user_bp)
auth_bp.register_blueprint(role_bp)
auth_bp.register_blueprint(authority_bp)


__all__ = ["auth_bp"]
