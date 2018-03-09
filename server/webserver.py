import tornado.web

# Handlers
import core.api.answers as answers_handler
import core.api.questions as questions_handler
import core.api.tags as tags_handler
import core.api.votes as votes_handler


class WebApplication(tornado.web.Application):

    def register_routes(self):
        return [
            (r'/answers/?', answers_handler.AnswerHandler),
            (r'/answers/(?P<answer_id>[0-9]+)', answers_handler.AnswerByIdHandler),
            (r'/questions/?', questions_handler.QuestionHandler),
            (r'/questions/(?P<question_id>[0-9]+)', questions_handler.QuestionByIdHandler),
            (r'/tags/?', tags_handler.TagHandler),
            (r'/tags/(?P<tag_id>[0-9]+)', tags_handler.TagByIdHandler),
            (r'/votes/?', votes_handler.VoteHandler),
            (r'/votes/(?P<tag_id>[0-9]+)', votes_handler.VoteByIdHandler),
        ]

    def __init__(self):

        # Register routes
        handlers = self.register_routes()
        
        # Init Tornado Application
        tornado.web.Application.__init__(self, handlers)


if __name__ == "__main__":
    app = WebApplication()
    app.listen(5000)
    tornado.ioloop.IOLoop.current().start()
