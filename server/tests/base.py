import json

from redislite import StrictRedis
from tornado.testing import AsyncHTTPTestCase

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
