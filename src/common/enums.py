from enum import Enum, IntEnum


class ResCode(IntEnum):
    SUCCESS = 0
    ERROR = 1


class Status(IntEnum):
    enable = 0
    disable = 1


class Gender(IntEnum):
    """ 性别类型 0: 未知 1：男 2：女"""
    unknown = 0
    male = 1
    female = 2


class FileUploadStatus(IntEnum):
    """
    文件上传状态
    """
    initial = 1
    uploading = 2
    finished = 3
    failed = 4


class CosAction(str, Enum):
    """ 只列出了对象存储操作 """
    # 查询对象元数据
    HeadObject = "name/cos:HeadObject"
    # 下载操作
    GetObject = "name/cos:GetObject"
    # 简单上传操作
    PutObject = "name/cos:PutObject",
    # 表单上传对象
    PostObject = "name/cos:PostObject",
    # 分块上传：初始化分块操作
    InitiateMultipartUpload = "name/cos:InitiateMultipartUpload",
    # 分块上传：List 进行中的分块上传
    ListMultipartUploads = "name/cos:ListMultipartUploads",
    # 分块上传：List 已上传分块操作
    ListParts = "name/cos:ListParts",
    # 分块上传：上传分块块操作
    UploadPart = "name/cos:UploadPart",
    # 分块上传：完成所有分块上传操作
    CompleteMultipartUpload = "name/cos:CompleteMultipartUpload",
    # 取消分块上传操作
    AbortMultipartUpload = "name/cos:AbortMultipartUpload"
