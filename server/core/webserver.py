import argparse
import logging
import logging.config
import sys

from sqlalchemy import engine_from_config
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from tornado.ioloop import IOLoop
from tornado.ioloop import PeriodicCallback
from tornado.web import Application

# Handlers
import core.api.answers as answers_handler
import core.api.authentication as authentication_handler
import core.api.init as init_handler
import core.api.ping as ping_handler
import core.api.questions as questions_handler
import core.api.search as search_handler
import core.api.tags as tags_handler
import core.api.users as users_handler
import core.api.votes as votes_handler

# Utils
from core.utils.config import parse_config
from core.services.redis import RedisClient
from core.session.store import SessionStore


class WebServer(Application):

    def register_routes(self):
        return [
            (r'/authenticated/?', authentication_handler.AuthenticatedHandler),
            (r'/init/?', init_handler.InitHandler),
            # Search
            (r'/search/?', search_handler.SearchHandler),
            # Questions
            (r'/questions/?', questions_handler.QuestionHandler),
            (r'/questions/(?P<question_id>[0-9]+)', questions_handler.QuestionByIdHandler),
            # Answers
            (r'/questions/(?P<question_id>[0-9]+)/answers/?', answers_handler.AnswerHandler),
            (r'/answers/(?P<answer_id>[0-9]+)', answers_handler.AnswerByIdHandler),
            # Votes
            (r'/answers/(?P<answer_id>[0-9]+)/votes/?', votes_handler.AnswerVoteHandler),
            (r'/questions/(?P<question_id>[0-9]+)/votes/?', votes_handler.QuestionVoteHandler),
            # Tags
            (r'/tags/?', tags_handler.TagHandler),
            # Users
            (r'/login/?', authentication_handler.LoginHandler),
            (r'/logout/?', authentication_handler.LogoutHandler),
            (r'/users/?', users_handler.UserHandler),
            # Others
            (r'/ping/?', ping_handler.PingHandler)
        ]

    def __init__(self, config):

        # Config
        self.config = config

        # Database
        self.db = scoped_session(sessionmaker(bind=engine_from_config({
            'sqlalchemy.url': config.get('sqlalchemy', 'url'),
            'sqlalchemy.echo': config.getboolean('sqlalchemy', 'echo')
        }), autoflush=True))

        # Init Redis
        self.redis_client = RedisClient.from_config(config)

        # Init Session Store
        self.session_store = SessionStore(
            redis_client=self.redis_client,
            expires=self.config.getint('answer', 'session_timeout_s'),
            is_secure=self.config.get('answer', 'env') == 'prod'
        )

        # Register periodic callback to cull sessions
        if IOLoop.current():
            scheduler = PeriodicCallback(
                self.session_store.cull,
                self.config.getint('answer', 'session_cull_interval_ms')
            )
            scheduler.start()

        # Register routes
        handlers = self.register_routes()

        # Init Tornado Application
        settings = {
            'debug': True if config.getint('tornado', 'debug') == 1 else False,
            'autoreload': True if config.getint('tornado', 'autoreload') == 1 else False,
            'cookie_secret': config.get('answer', 'cookie_secret')
        }
        Application.__init__(self, handlers, **settings)


if __name__ == "__main__":

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', dest='config', required=True)
    args = parser.parse_args()
    if not args.config:
        parser.print_help()
        sys.exit(1)

    # Get config
    config = parse_config(args.config)

    # Set logging config
    logging.config.fileConfig(config, disable_existing_loggers=0)

    # Launch webserver
    app = WebServer(config)
    app.listen(5000)
    IOLoop.current().start()
