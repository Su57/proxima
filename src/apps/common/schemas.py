# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 21/10/12 15:44
# @Description   :
from dataclasses import dataclass

from pydantic import Field, EmailStr

from src.core.config.serializer import BaseSerializationSchema, BaseValidationSchema


class LoginSchema(BaseValidationSchema):
    """ 登录 """
    email: EmailStr = Field(..., description="邮箱")
    password: str = Field(..., description="密码")


@dataclass(frozen=True)
class BearerToken(BaseSerializationSchema):
    access_token: str
    token_type: str
    expired_at: int


@dataclass
class FileViewSchema:
    id: int
    url: str
    size: int
    filename: str


__all__ = ["LoginSchema", "BearerToken", "FileViewSchema"]
