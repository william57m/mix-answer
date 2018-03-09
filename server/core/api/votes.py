from tornado.web import RequestHandler


class VoteHandler(RequestHandler):

    def get(self):
        self.write("VoteHandler: GET")

    def post(self):
        self.write("VoteHandler: POST")


class VoteByIdHandler(RequestHandler):

    def get(self, answer_id):
        self.write("VoteByIdHandler: GET")

    def put(self, answer_id):
        self.write("VoteByIdHandler: PUT")

    def delete(self, answer_id):
        self.write("VoteByIdHandler: DELETE")
