# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 21/10/11 11:52
# @Description   :
import pathlib
from os import PathLike
from typing import List, Optional
from urllib.parse import urljoin

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, request, send_file

from container import Container
from settings import settings
from src.apps.common.models import File
from src.apps.common.schemas import FileViewSchema
from src.apps.common.services import FileService
from src.core.security import login_required
from src.core.web.response import Response

bp = Blueprint("file", __name__, url_prefix="/file")


@bp.post("/upload")
@login_required
@inject
def upload(service: FileService = Provide[Container.file_service]):
    """
    上传文件 WARNING: 只有使用本地文件服务时，才可以使用此接口
    """
    result: List[FileViewSchema] = []
    files = request.files
    for item in files.items():
        _, file_storage = item
        file = service.upload(file_storage)
        # 需要重新组装文件URL
        file.url = urljoin(request.host_url, file.url)
        result.append(file)
    return Response.ok(data=result)


@bp.get("/download/<int:ident>")
@login_required
@inject
def download(ident: int, service: FileService = Provide[Container.file_service]):
    """
    下载本地文件 WARNING: 只有使用本地文件服务时，才可以使用此接口

    :param ident: 文件id
    :param service:
    :return:
    """
    file: Optional[File] = service.get_by_id(ident)
    if file is None:
        return Response.error(msg="文件不存在")
    file_path: PathLike = pathlib.Path(settings.BASE_DIR, settings.UPLOAD_DIR, file.key)
    mimetype: str = file.content_type.split(";")[0]
    return send_file(file_path, as_attachment=True, attachment_filename=file.filename, mimetype=mimetype)


@bp.delete("/download/<int:ident>")
@login_required
@inject
def delete(ident: int, service: FileService = Provide[Container.file_service]):
    """
    删除文件

    :param ident: 文件id
    :param service:
    :return:
    """
    return service.delete(ident)
