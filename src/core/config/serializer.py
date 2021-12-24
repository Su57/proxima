import orjson
from pydantic import BaseConfig, BaseModel, Extra


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class SerializationConfig(BaseConfig):
    """ 用于进行序列化的schema """
    orm_mode = True
    json_loads = orjson.loads
    json_dumps = orjson_dumps
    use_enum_values = True


class BaseSerializationSchema(BaseModel):
    """ pydantic序列化配置 """
    class Config:
        orm_mode = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        use_enum_values = True


class BaseValidationSchema(BaseModel):
    class Config:
        extra = Extra.ignore
        # 直接使用enum的value
        use_enum_values = True
        # 去除str和byte的首位空白符
        anystr_strip_whitespace = True
        # 带下划线的是否为受保护字段
        underscore_attrs_are_private = True
        # 存在别名的情况下允许通过原始名进行字段赋值
        allow_population_by_field_name = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps
