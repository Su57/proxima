from flask import Blueprint, request
from dependency_injector.wiring import inject, Provide

from src.apps.manage.models import User

from src.utils import RequestUtil
from src.core.web.schemas import Page
from src.common.constant import Constant
from container import Container
from src.core.web.response import Response
# from src.core.security import login_required
from src.apps.manage.services import UserService
from src.apps.manage.schemas import UserCreateSchema, UserUpdateSchema, UserViewSchema

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.get("/page")
@inject
# @login_required
def page(service: UserService = Provide[Container.user_service]) -> Response[Page[UserViewSchema]]:
    """ 获取用户分页列表 """
    current: int = RequestUtil.parse_int_arg("current", default=Constant.CURRENT_PAGE)
    size: int = RequestUtil.parse_int_arg("size", default=Constant.PAGE_SIZE)
    data: Page[UserViewSchema] = service.get_user_list(current=current, size=size)
    return Response.ok(data=data)


@bp.get("/info/<int:ident>")
@inject
# @login_required
def info(ident: int, service: UserService = Provide[Container.user_service]) -> Response[UserViewSchema]:
    user: User = service.get_by_id(ident)
    return Response.ok(data=UserViewSchema.from_orm(user))


@bp.post("/add")
@inject
# @login_required
def add(service: UserService = Provide[Container.user_service]) -> Response[str]:
    schema: UserCreateSchema = UserCreateSchema(**request.json)
    service.add_user(schema)
    return Response.ok(msg="用户添加成功")


@bp.post("/update/<int:ident>")
@inject
# @login_required
def update(ident: int, service: UserService = Provide[Container.user_service]) -> Response[str]:
    # schema = service.validate_data(request.json, UserUpdateSchema)
    schema: UserUpdateSchema = UserUpdateSchema(**request.json)
    service.update_user(ident, schema)
    return Response.ok(msg="用户修改成功")


@bp.delete("/delete/<int:ident>")
@inject
# @login_required
def delete(ident: int, service: UserService = Provide[Container.user_service]) -> Response[str]:
    service.delete_user(ident)
    return Response.ok(msg="用户删除成功")
