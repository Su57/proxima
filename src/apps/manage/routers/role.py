from flask import Blueprint, request
from dependency_injector.wiring import inject, Provide

from src.utils import RequestUtil
from src.apps.manage.models import Role
from src.core.web.schemas import Page
from src.common.constant import Constant
from container import Container
from src.core.web.response import Response
from src.apps.manage.services.role import RoleService
from src.apps.manage.schemas import RoleCreateSchema, RoleUpdateSchema, RoleViewSchema


bp = Blueprint("role", __name__, url_prefix="/role")


@bp.get("/page")
@inject
# @login_required
def page(service: RoleService = Provide[Container.role_service]) -> Response[Page[RoleViewSchema]]:
    current: int = RequestUtil.parse_int_arg("current", default=Constant.CURRENT_PAGE)
    size: int = RequestUtil.parse_int_arg("size", default=Constant.PAGE_SIZE)
    data: Page[Role] = service.get_page(current, size)
    data.records = [RoleViewSchema.from_orm(role) for role in data.records]
    return Response.ok(data=data)


@bp.get("/info/<int:ident>")
@inject
# @login_required
def info(ident: int, service: RoleService = Provide[Container.role_service]) -> Response[RoleViewSchema]:
    role: RoleViewSchema = RoleViewSchema.from_orm(service.get_by_id(ident))
    return Response.ok(data=role)


@bp.post("/add")
@inject
# @login_required
def add(service: RoleService = Provide[Container.role_service]) -> Response:
    schema = RoleCreateSchema(**request.json)
    service.add_role(schema)
    return Response.ok(msg="角色创建成功")


@bp.post("/update/<int:ident>")
@inject
# @login_required
def update(ident: int, service: RoleService = Provide[Container.role_service]) -> Response:
    schema = RoleUpdateSchema(**request.json)
    service.update_role(ident, schema)
    return Response.ok(msg="角色更新成功")


@bp.delete("/delete/<int:ident>")
@inject
# @login_required
def delete(ident: int, service: RoleService = Provide[Container.role_service]) -> Response:
    service.delete_role(ident)
    return Response.ok(msg="角色删除成功")
