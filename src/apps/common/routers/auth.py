from flask import Blueprint, request
from dependency_injector.wiring import inject, Provide

from container import Container
from src.core.web.response import Response
from src.apps.common.services.auth import AuthService
from src.apps.common.schemas import BearerToken, LoginSchema

bp: Blueprint = Blueprint("auth", __name__)


@bp.post("/login")
@inject
def login(auth_service: AuthService = Provide[Container.auth_service]) -> BearerToken:
    """ 登录 """
    # 检验验证码
    body: LoginSchema = LoginSchema(**request.json)
    # 执行登录，获取令牌
    token: BearerToken = auth_service.authenticate(email=body.email, password=body.password)
    return Response.ok(data=token)
