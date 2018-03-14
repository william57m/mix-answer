import datetime
import hashlib
import logging

from core.services.redis import RedisKeys
from core.utils import date

log = logging.getLogger(__name__)

SESSION_HASH_LENGTH = 20


class Session:

    def __init__(self, session_id, redis_client, user_id=None):
        self.session_id = session_id
        self.redis_client = redis_client
        self.user_id = user_id
        self._created = datetime.datetime.utcnow()
        self._last_accessed = self._created

    # Properties
    @property
    def session_hash(self):
        """ Return a hash of the session ID """
        return self.hash_session_id(self.session_id)

    @property
    def redis_session_key(self):
        """ Return the key as it is stored in Redis with the session ID """
        return RedisKeys.session_info.format(session_id=self.session_id)

    @property
    def is_authenticated(self):
        """ Return the user state """
        return self.user_id is not None

    @property
    def redis_representation(self):
        """
        Return session representation required for storage in Redis.
        This returns the format of the stored session in the Redis DB.
        """
        return {
            'name': self.redis_session_key,
            'mapping': {
                'user_id': self.user_id,
                '__meta__created_at': date.format_datetime_object(self._created),
                '__meta__last_accessed_at': date.format_datetime_object(self._last_accessed),
            }
        }

    def to_dict(self):
        return {
            'session_id': self.session_id,
            'user_id': self.user_id,
            '_created': date.format_datetime_object(self._created),
            '_last_accessed': date.format_datetime_object(self._last_accessed)
        }

    # Methods for properties
    @classmethod
    def hash_session_id(cls, session_id):
        return hashlib.sha512(
            session_id.encode('utf-8')
        ).hexdigest()[:SESSION_HASH_LENGTH]

    @classmethod
    def from_redis(cls, redis_client, redis_repr):
        """ Create a Session object from its representation in the Redis DB """
        session_id = redis_repr.get('name').split(':', 1)[1]
        session_info = redis_repr.get('mapping')
        user_id = cls.extract_user(session_info)

        session = cls(session_id=session_id, redis_client=redis_client, user_id=user_id)
        session._created = date.get_datetime_object(session_info.get('__meta__created_at'))
        session._last_accessed = date.get_datetime_object(session_info.get('__meta__last_accessed_at'))
        return session

    @staticmethod
    def extract_user(session_info):
        user_id = session_info.get('user_id')
        try:
            user_id = int(user_id)
        except Exception:
            user_id = None
        return user_id

    def register_accessed(self):
        """ Update the last access timestamp to the current time """
        self._last_accessed = datetime.datetime.utcnow()
        self.save()

    def save(self):
        """ Save the session into the Redis DB """
        return self.redis_client.hmset(**self.redis_representation)

    def invalidated(self, expires_in_seconds):
        """
        Return whether or not the session has been invalidated.
        A session is considered invalidated if the time between
        NOW and LAST_ACCESSED is greater than EXPIRY duration
        """
        now = datetime.datetime.utcnow()
        time_since_access = (now - self._last_accessed)
        expires_td = datetime.timedelta(seconds=expires_in_seconds)
        return time_since_access >= expires_td
