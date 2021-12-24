from typing import List, Dict, Any

from flask import Blueprint, request
from dependency_injector.wiring import inject, Provide

from container import Container
from src.core.web.response import Response
from src.apps.manage.models import Authority
from src.apps.manage.services import AuthorityService
from src.apps.manage.schemas import AuthorityViewSchema, AuthorityCreateSchema, AuthorityUpdateSchema


bp = Blueprint("perm", __name__, url_prefix="/perm")


@bp.get("/tree")
# @login_required
@inject
def tree(service: AuthorityService = Provide[Container.authority_service]) -> Response[AuthorityViewSchema]:
    authorities: List[Authority] = service.get_by_map(None)
    trees: List[Dict[str, Any]] = service.build_authority_tree(authorities)
    return Response.ok(data=trees)


@bp.post("/add")
# @login_required
@inject
def add(service: AuthorityService = Provide[Container.authority_service]):
    """ 添加新menu """
    data = AuthorityCreateSchema(**request.json)
    service.save(data)
    return Response.ok(msg="权限添加成功")


@bp.get("/info/<int:ident>")
# @login_required
@inject
def info(ident: int, service: AuthorityService = Provide[Container.authority_service]):
    """ 获取权限详细细信息 """
    perm = service.get_by_id(ident)
    return Response.ok(data=AuthorityViewSchema.from_orm(perm))


@bp.post("/update/<int:ident>")
# @login_required
@inject
def update(ident: int, service: AuthorityService = Provide[Container.authority_service]):
    data = AuthorityUpdateSchema(**request.json)
    service.update(ident, data)
    return Response.ok(msg="权限更新成功")


@bp.delete("/delete/<int:ident>")
# @login_required
@inject
def delete(ident: int, service: AuthorityService = Provide[Container.authority_service]):
    service.delete_authority(ident)
    return Response.ok(msg="删除成功")
