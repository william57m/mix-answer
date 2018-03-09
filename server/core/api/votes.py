from tornado.web import RequestHandler


class VoteHandler(RequestHandler):

    async def get(self):
        self.write("VoteHandler: GET")

    async def post(self):
        self.write("VoteHandler: POST")


class VoteByIdHandler(RequestHandler):

    async def get(self, answer_id):
        self.write("VoteByIdHandler: GET")

    async def put(self, answer_id):
        self.write("VoteByIdHandler: PUT")

    async def delete(self, answer_id):
        self.write("VoteByIdHandler: DELETE")
