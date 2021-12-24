from flask import Flask, Blueprint
from pydantic import ValidationError

from settings import settings
from container import Container
from src.exceptions import ProximaException
from src.apps.manage.routers import auth_bp
from src.apps.common.routers import common_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(settings)
    # 注册容器
    _register_container(app)
    # 注册蓝图
    _register_blueprints(app)
    # 注册异常处理程序
    _register_error_handler(app)
    return app


def _register_container(app: Flask) -> None:
    """ 注册容器 """
    container = Container()
    container.init_resources()
    app.container = container


def _register_blueprints(app: Flask) -> None:
    """ 注册蓝图 """
    # 统一注册所有路由
    bp = Blueprint("proxima", __name__)
    bp.register_blueprint(common_bp)
    bp.register_blueprint(auth_bp)
    app.register_blueprint(bp)


def _register_error_handler(app: Flask) -> None:
    """ 注册异常处理程序 """

    @app.errorhandler(Exception)
    def handler(exc) -> ProximaException:
        if isinstance(exc, ProximaException):
            return exc
        elif isinstance(exc, ValidationError):
            return ProximaException(error_code=2, code=400, description="参数错误", data=exc.errors())
        else:
            return ProximaException(error_code=2, code=400, description=str(exc))


application = create_app()


if __name__ == '__main__':
    application.run(port=5000, host="0.0.0.0", debug=True)
