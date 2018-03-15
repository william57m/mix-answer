import json

from redislite import StrictRedis
from tornado.testing import AsyncHTTPTestCase
from tornado.web import create_signed_value

from core.db.models import User
from core.session.model import Session
from core.webserver import WebServer
from core.utils.config import parse_config


app = None
config = parse_config('config/test.conf')
redis_server = StrictRedis(decode_responses=True)
config.set('redis', 'socket', redis_server.socket_file)


def end_transactions(session):
    session.rollback() if session else None


def get_global_app():
    global app
    app = WebServer(config=config) if app is None else app
    return app


class BaseAppTestCase(AsyncHTTPTestCase):

    def setUp(self):
        super().setUp()
        self.addCleanup(end_transactions, session=self.db)

    # Need to be overrided by Tornado
    def get_app(self):
        return get_global_app()

    # Properties
    @property
    def app(self):
        return self.get_app()

    @property
    def db(self):
        return self.app.db

    # Useful methods
    @staticmethod
    def response_dict(response):
        return json.loads(response.body.decode('utf-8')) if response.body else None


class AuthAppTestCase(BaseAppTestCase):

    USER_DATA = {
        'firstname': 'User',
        'lastname': 'Name',
        'email': 'user.name@mixanswer.com'
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request_user = None
        self.session = None
        self.headers = None

    def setUp(self):
        super().setUp()
        self._init_user()

    def tearDown(self):
        self._remove_users()
        if self.session:
            self.app.session_store.delete_sessions(self.session.session_id)
        super().tearDown()

    def _auth_user(self, user):
        app = self.app

        # Generate a session ID
        session_id = app.session_store.generate_session_id()
        if self.session:
            app.session_store.delete_sessions(self.session.session_id)
        self.session = Session(session_id=session_id, redis_client=app.session_store.redis_client, user_id=user.id)
        app.session_store.add_session(self.session)

        # Generate a cookie associated to the created session ID
        cookie_name, cookie_value = app.session_store.COOKIE_NAME, str(session_id)
        secure_cookie = create_signed_value(app.settings['cookie_secret'], cookie_name, cookie_value).decode('utf-8')
        headers = {'Cookie': '='.join((cookie_name, secure_cookie))}
        return headers

    def _init_user(self):
        email = self.USER_DATA['email']
        user = self.db.query(User).filter_by(email=email).first()
        if not user:
            self.request_user = User(**self.USER_DATA)
            self.db.add(self.request_user)
            self.db.commit()
        else:
            self.request_user = user

        self.db.commit()

    def _remove_users(self):
        self.db.query(User).delete()
        self.db.commit()
        self.users = {}

    def fetch(self, *args, **kwargs):
        if kwargs.get('headers') is not None:
            self.headers = kwargs.get('headers')
        else:
            self._set_headers()

        headers = self.headers.copy()
        kwargs['headers'] = headers
        return super().fetch(*args, **kwargs)

    def _set_headers(self):
        self.headers = self._auth_user(self.request_user)
        self.headers['Content-Type'] = 'application/json'
