from sqlalchemy.exc import SQLAlchemyError

from core.db.models import User
from core.services.ldap import LDAPClient


class Authentication:

    def __init__(self, application):
        self.application = application

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

                return user

        return None

    def regular_auth(self, email, password):
        user = self.application.db.query(User).filter(User.email == email) \
                                              .filter(User.password == password) \
                                              .first()
        return user

    async def login(self, email, password):
        user = None
        if self.application.config.getboolean('ldap', 'enabled'):
            user = await self.ldap_auth(email, password)
        else:
            user = await self.regular_auth(email, password)

        return user
