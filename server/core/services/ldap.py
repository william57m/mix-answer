import ldap3
import logging

log = logging.getLogger(__name__)


class LDAPConfig:
    def __init__(self, config, email=None, password=None):
        self.ldap_version = config.get('ldap', 'version')
        self.ldap_server = config.get('ldap', 'server')
        self.ldap_user = email or config.get('ldap', 'user')
        self.ldap_password = password or config.get('ldap', 'password')
        self.ldap_base_dn = config.get('ldap', 'base_dn')
        self.ldap_search_template = config.get('ldap', 'search_template')
        self.attributes = ['cn', 'sn', 'givenName', 'description', 'countryCode', 'department', 'title', 'telephoneNumber']


class LDAPClient:
    def __init__(self, config, email=None, password=None):
        self.raw_config = config
        self.config = LDAPConfig(config, email, password)
        self.server = ldap3.Server(self.config.ldap_server)
        self.connection = ldap3.Connection(
            self.config.ldap_server,
            user=self.config.ldap_user,
            password=self.config.ldap_password,
            auto_bind=True
        )

    def connect(self):
        ldap_client = None
        try:
            ldap_client = LDAPClient(self.raw_config)
        except Exception as exception:
            log.exception(f"Couldn't connect to LDAP ${self.config['ldap_server']}")

        return ldap_client

    def login(self, email, password):
        ldap_client = None
        try:
            ldap_client = LDAPClient(self.raw_config, email, password)
        except Exception as exception:
            return None

        return ldap_client

    def search_user(self, email):
        query = self.config.ldap_search_template % email
        return self.connection.search(self.config.ldap_base_dn,
                                      query,
                                      ldap3.SEARCH_SCOPE_WHOLE_SUBTREE,
                                      attributes=self.config.attributes)

    def get_user(self, email):
        result = None
        ldap_client = self.connect()

        if ldap_client and ldap_client.search_user(email):
            entries = ldap_client.connection.response
            result = entries[0] if len(entries) > 0 else None

        return result
