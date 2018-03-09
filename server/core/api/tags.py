from tornado.web import RequestHandler


class TagHandler(RequestHandler):

    async def get(self):
        self.write("TagHandler: GET")

    async def post(self):
        self.write("TagHandler: POST")


class TagByIdHandler(RequestHandler):

    async def get(self, answer_id):
        self.write("TagByIdHandler: GET")

    async def put(self, answer_id):
        self.write("TagByIdHandler: PUT")

    async def delete(self, answer_id):
        self.write("TagByIdHandler: DELETE")
