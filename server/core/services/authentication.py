import functools
import logging

from sqlalchemy.exc import SQLAlchemyError

from core.db.models import User
from core.services.ldap import LDAPClient
from core.utils.exceptions import UnauthenticatedError

log = logging.getLogger(__name__)


class AuthenticationService:

    def __init__(self, request_handler):
        self.request_handler = request_handler
        self.application = request_handler.application

    def get_user_by_email(self, email):
        user = self.application.db.query(User).filter(User.email == email).first()
        return user

    def register_user(self, user_dict):
        user = User(**user_dict)

        # Commit in DB
        try:
            self.application.db.add(user)
            self.application.db.commit()
        except SQLAlchemyError as error:
            self.application.db.rollback()

        return user

    def register_session(self, user):
        new_session = self.application.session_store.regenerate(self.request_handler, user.id)
        return new_session

    async def ldap_auth(self, email, password, id_token=None):
        user = None

        ldap_client = LDAPClient(self.application.config)
        user_entry = ldap_client.get_user(email)

        if user_entry:
            ldap_user = user_entry['dn']
            ldap_password = password

            if ldap_client.login(email=ldap_user, password=ldap_password):
                user_attrs = user_entry['attributes']
                user_dict = {
                    'email': email,
                    'firstname': user_attrs['givenName'][0],
                    'lastname': user_attrs['sn'][0] if 'sn' in user_attrs else 'Service'
                }
                user = self.get_user_by_email(user_dict['email'])
                if not user:
                    user = self.register_user(user_dict)

                # Regenerate session
                self.register_session(user)

                return user

        return None

    def regular_auth(self, email, password):
        # Find user
        user = self.application.db.query(User).filter(User.email == email) \
                                              .filter(User.password == password) \
                                              .first()
        # Regenerate session
        if user:
            self.register_session(user)

        return user

    async def login(self, email, password):
        user = None
        if self.application.config.getboolean('ldap', 'enabled'):
            user = await self.ldap_auth(email, password)
        else:
            user = await self.regular_auth(email, password)

        return user

    async def logout(self):
        self.application.session_store.unregister(self.request_handler)

    @classmethod
    def requires_login(cls, func):
        """
        Creates a decorator to validate there is a logged in user
        """
        @functools.wraps(func)
        def _requires_login(handler, *args, **kwargs):
            if not handler.user:
                raise UnauthenticatedError()
            else:
                return func(handler, *args, **kwargs)
        return _requires_login
