import argparse
import sys

from sqlalchemy import engine_from_config
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from tornado.ioloop import IOLoop
from tornado.web import Application

# Handlers
import core.api.answers as answers_handler
import core.api.questions as questions_handler
import core.api.tags as tags_handler
import core.api.users as users_handler
import core.api.votes as votes_handler

# Utils
from core.utils.config import parse_config


class WebServer(Application):

    def register_routes(self):
        return [
            # Questions
            (r'/questions/?', questions_handler.QuestionHandler),
            (r'/questions/(?P<question_id>[0-9]+)', questions_handler.QuestionByIdHandler),
            # Answers
            (r'/questions/(?P<question_id>[0-9]+)/answers/?', answers_handler.AnswerHandler),
            (r'/answers/(?P<answer_id>[0-9]+)', answers_handler.AnswerByIdHandler),
            # Votes
            (r'/answers/(?P<answer_id>[0-9]+)/votes/?', votes_handler.VoteHandler),
            # Tags
            (r'/tags/?', tags_handler.TagHandler),
            (r'/tags/(?P<tag_id>[0-9]+)', tags_handler.TagByIdHandler),
            (r'/users/?', users_handler.UserHandler),
            (r'/users/(?P<vote_id>[0-9]+)', users_handler.UserByIdHandler)
        ]

    def __init__(self, config):

        # Database
        self.db = scoped_session(sessionmaker(bind=engine_from_config({
            'sqlalchemy.url': config.get('sqlalchemy', 'url'),
            'sqlalchemy.echo': config.getboolean('sqlalchemy', 'echo')
        }), autoflush=True))

        # Register routes
        handlers = self.register_routes()

        # Init Tornado Application
        settings = {
            'debug': True if config.getint('tornado', 'debug') == 1 else False,
            'autoreload': True if config.getint('tornado', 'autoreload') == 1 else False
        }
        Application.__init__(self, handlers, **settings)


if __name__ == "__main__":

    # Config
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', dest='config', required=True)
    args = parser.parse_args()
    if not args.config:
        parser.print_help()
        sys.exit(1)
    config = parse_config(args.config)

    app = WebServer(config)
    app.listen(5000)
    IOLoop.current().start()
