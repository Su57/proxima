from src.apps.common.models import File
from src.core.repository import Repository


class FileRepository(Repository[File]):
    entity_class = File


__all__ = ["FileRepository"]
