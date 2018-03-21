import tornado.web


class PingHandler(tornado.web.RequestHandler):

    async def get(self):
        self.set_status(204)
        self.finish()
