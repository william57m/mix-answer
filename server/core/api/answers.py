from tornado.web import RequestHandler


class AnswerHandler(RequestHandler):

    def get(self):
        self.write("AnswerHandler: GET")

    def post(self):
        self.write("AnswerHandler: POST")


class AnswerByIdHandler(RequestHandler):

    def get(self, answer_id):
        self.write("AnswerByIdHandler: GET")

    def put(self, answer_id):
        self.write("AnswerByIdHandler: PUT")

    def delete(self, answer_id):
        self.write("AnswerByIdHandler: DELETE")
