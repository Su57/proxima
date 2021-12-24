from typing import AnyStr, Generator

from redis import Redis


def get_redis(dsn: AnyStr, max_connections: int) -> Generator[Redis, None, None]:
    client: Redis = Redis.from_url(dsn, decode_responses=True, max_connections=max_connections)
    try:
        yield client
    finally:
        client.close()
        client.connection_pool.disconnect()
