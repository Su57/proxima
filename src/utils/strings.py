import re
from dataclasses import dataclass
from typing import Optional
from uuid import uuid4, UUID


@dataclass
class StringBuilder:

    """ 字符串拼接工具 """
    content: Optional[str] = ""

    def append_line(self, stm: str):
        self.content += stm + "\n"


class StringUtil:

    @staticmethod
    def get_unique_key() -> str:
        """ 获取全局唯一key(去除中划线) """
        unique_key: UUID = uuid4()
        return unique_key.hex

    @staticmethod
    def remove_blank(raw_string: str) -> str:
        """ 去除字符串中的空白符 """
        return re.sub(r"\s", "", raw_string)
