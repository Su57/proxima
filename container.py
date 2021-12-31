from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import ThreadSafeSingleton, Resource, Factory, Dependency

from settings import settings
from src.apps.common.repository import *
from src.apps.common.services import *
from src.apps.manage.repository import *
from src.apps.manage.services import *
from src.core.db.session import SessionFactory, SessionContext
from src.core.redis import get_redis


class Container(DeclarativeContainer):
    """ IOC 容器"""

    wiring_config = WiringConfiguration(packages=["src"])

    redis = Resource(
        get_redis,
        dsn=settings.REDIS_DSN,
        max_connections=settings.REDIS_MAX_CONNECTIONS
    )

    session_factory = ThreadSafeSingleton(
        SessionFactory,
        dsn=settings.SQLALCHEMY_DATABASE_URI
    )

    session_context = Factory(
        SessionContext,
        factory=session_factory
    )

    auth_service = Dependency(
        instance_of=AuthService,
        default=Factory(
            AuthServiceImpl,
            redis=redis,
            repository=Factory(
                UserRepository,
                session_context=session_context
            )
        )
    )

    file_service = Dependency(
        instance_of=FileService,
        default=Factory(
            LocalFileService,
            repository=Factory(
                FileRepository,
                session_context=session_context
            )
        )
    )

    user_service = Dependency(
        instance_of=UserService,
        default=Factory(
            UserServiceImpl,
            repository=Factory(
                UserRepository,
                session_context=session_context
            )
        )
    )

    role_service = Dependency(
        instance_of=RoleService,
        default=Factory(
            RoleServiceImpl,
            repository=Factory(
                RoleRepository,
                session_context=session_factory
            )
        )
    )

    authority_service = Dependency(
        instance_of=AuthorityService,
        default=Factory(
            AuthorityServiceImpl,
            repository=Factory(
                AuthorityRepository,
                session_context=session_context
            )
        )
    )
