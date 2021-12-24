# -*- coding: utf-8 -*-
# @Author        : Yao YuHang
# @CreatedTime   : 2021/1/29 16:21
# @Description   :
from typing import Any, Dict
from datetime import timedelta, datetime

from jose.constants import ALGORITHMS
from jose import jwt, ExpiredSignatureError, JWTError
from werkzeug.security import generate_password_hash, check_password_hash

from settings import settings
from src.exceptions import TokenExpiredException, UnAuthorizedException


class SecurityUtil:

	""" 安全相关的功能集合 """

	@staticmethod
	def create_token(subject: Any, expires_delta: timedelta = None) -> str:
		"""
		签发token

		:param subject: token信息
		:param expires_delta: 过期时间
		:return:
		"""
		if expires_delta:
			expire = datetime.utcnow() + expires_delta
		else:
			expire = datetime.utcnow() + timedelta(minutes=settings.TOKEN_EXPIRED_MINUTES)
		payload = {"exp": expire, "sub": str(subject)}
		token = jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHMS.HS256)
		return token

	@staticmethod
	def parse_token(token: str) -> Dict:
		"""
		解析token, 获取token携带的信息

		:param token: 待解析的token
		:return: 解析后的信息
		"""
		try:
			return jwt.decode(token, key=settings.SECRET_KEY, algorithms=[ALGORITHMS.HS256])
		# 令牌过期
		except ExpiredSignatureError:
			raise TokenExpiredException
		# 无效令牌
		except JWTError:
			raise UnAuthorizedException("无效的身份信息")

	@classmethod
	def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
		"""
		校验密码

		:param plain_password: 明文码
		:param hashed_password: 哈希码
		:return: 是否匹配
		"""
		return check_password_hash(hashed_password, plain_password)

	@classmethod
	def generate_password(cls, password: str) -> str:
		"""
		生成密码

		:param password: 明文码
		:return: 哈希码
		"""
		return generate_password_hash(password)
