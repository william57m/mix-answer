import logging
import uuid

from core.session.model import Session
from core.services.redis import RedisKeys

log = logging.getLogger(__name__)


class SessionStore:
    """
    The SessionStore handles registering and accessing the sessions.

    A SessionStore is linked to a Redis DB that provides
    interfaces for write operations (add/edit|save/remove) as well as
    read operations (get). Some of these functionalities are wrapped to
    correspond with the way we store and interpret sessions internally.

    The store contains method to cull, which should be invoked periodically.
    """

    COOKIE_NAME = '_mixanswer'

    def __init__(self, redis_client, expires=1800, is_secure=False):
        self.expires = expires
        self.is_secure = is_secure
        self.redis_client = redis_client

    def __len__(self):
        """ Gets the number of sessions in the store. """
        count = 0
        for _key in self.redis_client.scan_iter(match='session:*'):
            count += 1
        return count

    @staticmethod
    def get_redis_key_repr(session_id):
        """ Returns the redis key associated with the given session_id """
        return RedisKeys.session_info.format(session_id=session_id)

    @staticmethod
    def generate_session_id():
        """ Generate a unique session ID """
        return str(uuid.uuid4())

    def get_redis_sessions(self, match_on='*'):
        """ Return a list of all the sessions in the Redis store """
        redis_sessions = []
        for key in self.redis_client.scan_iter(match=f'session:{match_on}'):
            val = self.redis_client.hgetall(key)
            redis_sessions.append({
                'name': key,
                'mapping': val
            })
        return redis_sessions

    def get_internal_sessions(self):
        return [Session.from_redis(self.redis_client, session) for session in self.get_redis_sessions()]

    def get_redis_session(self, session_id):
        return self.redis_client.hgetall(self.get_redis_key_repr(session_id))

    def get_internal_session(self, session_id):
        session_info = self.get_redis_session(session_id)
        if session_info:
            redis_repr = {
                'name': self.get_redis_key_repr(session_id),
                'mapping': session_info
            }
            return Session.from_redis(redis_client=self.redis_client,
                                      redis_repr=redis_repr)
        return None

    def register(self, request_handler, user_id=None):
        """Explicitly create and register a new session"""
        session_id = self.generate_session_id()
        log.info('Created a new session [%s]', session_id)

        # Create and Store new session in Redis DB
        session = Session(session_id=session_id,
                          redis_client=self.redis_client,
                          user_id=user_id)
        self.add_session(session)

        request_handler.set_secure_cookie(**self.get_cookie_info(session_id))
        request_handler._session_id = session_id

        # For the case when the session is registered more than once while
        # handling the same HTTP operation (cf. `BaseRequestHandler#session`)...
        request_handler.__session__ = session
        return session

    def get_cookie_info(self, session_id):
        cookie_info = {
            'name': self.COOKIE_NAME,
            'value': session_id,
            'httponly': True,
            'expires_days': None,
        }
        if self.is_secure is True:
            cookie_info['secure'] = True
        return cookie_info

    def unregister(self, request_handler):
        """Clear the session cookie and delete it, if present"""
        unregistered = False

        # For the case when the session is registered then unregistered while
        # handling the same HTTP operation...
        request_handler.clear_cookie(self.COOKIE_NAME)

        session_id = request_handler.get_secure_cookie(self.COOKIE_NAME)
        if session_id:
            log.debug("Unregistering session: %s", session_id)
            session_id = session_id.decode('utf-8')
            unregistered = self.delete_sessions(session_id) == 1
            request_handler.clear_cookie(self.COOKIE_NAME)

        return unregistered

    def get(self, request_handler, auto_register=True):
        """
        If a session exists, access it; if it doesn't, create it
        Lookup request handler's cached session id, if absent try retrieving it from the cookies
        """
        session_id = self.get_cached_session_id(request_handler) or self.get_session_id_from_cookies(request_handler)
        session = self.get_internal_session(session_id)

        # If there is no session at this point, we create one
        if session is None:
            if auto_register:
                log.debug("Session '%s' doesn't exist, creating a new one...", session_id)
                session = self.register(request_handler)
        else:
            session.register_accessed()

        return session

    def add_session(self, session_object):
        """
        Ability to add a session object to the Redis DB.

        This will take in a session object, get the required
        representation for storage in Redis and finally save the info.
        """
        redis_repr = session_object.redis_representation
        redis_response = self.redis_client.hmset(**redis_repr)
        return redis_response

    def delete_sessions(self, *keys, ids_only=True):
        """
        Wrap the existing Redis 'DEL' functionality.

        This is a convenience method that takes care of updating the counter
        that represents the number of sessions we have in Redis whenever
        a session is deleted.
        """
        session_keys = [self.get_redis_key_repr(session_id) for session_id in keys] if ids_only else keys
        deleted_count = self.redis_client.delete(*session_keys)
        return deleted_count

    def delete_redis_session_pattern(self, pattern='*'):
        matched_sessions = []
        for key in self.redis_client.scan_iter(match=f'session:{pattern}'):
            matched_sessions.append(key)
        return self.delete_sessions(*matched_sessions, ids_only=False)

    @classmethod
    def get_cached_session_id(cls, request_handler):
        if hasattr(request_handler, '_session_id'):
            return request_handler._session_id
        else:
            return None

    @classmethod
    def get_session_id_from_cookies(cls, request_handler):
        """
        Try retrieving the encoded session id from the secure cookie.

        Uses tornado built-in method. If it fails but the session cookie is
        seemingly present, use the more permissive `cookies` lib.
        """
        encoded_session_id = request_handler.get_cookie(cls.COOKIE_NAME)

        if encoded_session_id is None:
            log.warn("Session could not be retrieved from cookie")

        session_id = request_handler.get_secure_cookie(name=cls.COOKIE_NAME, value=encoded_session_id)
        if session_id:
            session_id = session_id.decode('utf-8')

        return session_id

    def regenerate(self, request_handler, user_id=None):
        """
        Generate and store a new session

        When logging in, there are two things that happen:
        https://www.owasp.org/index.php/Session_Management_Cheat_Sheet#Domain_and_Path_Attributes
        - a new cookie is created, to enhance security per OWASP standards
        """
        unregistered = self.unregister(request_handler)
        if not unregistered:
            log.warn("Couldn't unregister existing session!")
        return self.register(request_handler, user_id)

    # Cleaning
    def cull(self):
        """Invalidate expired sessions.

        All sessions that have expired will be removed from the storage,
        and for sessions associated to a user (vs. "anonymous" sessions)
        we send a Pub/Sub message so the user can be notified and appropriately
        logged out.
        """
        sessions = self.get_internal_sessions()
        log.debug('<!> Starting session cull operation (%d session(s))', len(sessions))
        sessions_to_cull = []
        for session in sessions:
            if session.invalidated(self.expires):
                sessions_to_cull.append(session)

        num_sessions_to_cull = len(sessions_to_cull)
        if num_sessions_to_cull > 0:
            deleted_count = self.delete_sessions(*[session.session_id for session in sessions_to_cull])
            if deleted_count == num_sessions_to_cull:
                log.debug(f'{deleted_count} sessions culled: {sessions_to_cull}')
            else:
                log.warning('Sessions were not successfully culled')
