from tornado.web import RequestHandler


class UserHandler(RequestHandler):

    async def get(self):
        self.write("UserHandler: GET")

    async def post(self):
        self.write("UserHandler: POST")


class UserByIdHandler(RequestHandler):

    async def get(self, answer_id):
        self.write("UserByIdHandler: GET")

    async def put(self, answer_id):
        self.write("UserByIdHandler: PUT")

    async def delete(self, answer_id):
        self.write("UserByIdHandler: DELETE")
