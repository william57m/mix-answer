import enum
import logging
import redis

log = logging.getLogger(__name__)

DEFAULT_REDIS_HOST = '0.0.0.0'
DEFAULT_REDIS_PORT = 6379
DEFAULT_REDIS_DB = 0


class RedisKeys(enum.auto):
    """
    Keys used in the Redis DB
    """

    session_info = 'session:{session_id}'


class RedisClient:
    """
    Service to open a new connection to the Redis DB.
    """

    @classmethod
    def from_config(cls, config):
        return cls.connect_to_redis(config)

    @staticmethod
    def connect_to_redis(config):
        """
        Start a Redis client given a config containing a `redis` section.
        Default values defined for the port (6379) and db (0) are those used by Redis.
        """

        connection_kwargs = {
            'decode_responses': True,
            'db': config.getint('redis', 'db', fallback=DEFAULT_REDIS_DB),
            'host': config.get('redis', 'host', fallback=DEFAULT_REDIS_HOST),
            'port': config.getint('redis', 'port', fallback=DEFAULT_REDIS_PORT)
        }

        log.info('Connecting to Redis: %s', connection_kwargs)
        redis_client = redis.StrictRedis(**connection_kwargs)
        log.info('Connected to Redis!')

        return redis_client
