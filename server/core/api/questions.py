from tornado.web import RequestHandler


class QuestionHandler(RequestHandler):

    def get(self):
        self.write("QuestionHandler: GET")

    def post(self):
        self.write("QuestionHandler: POST")


class QuestionByIdHandler(RequestHandler):

    def get(self, answer_id):
        self.write("QuestionByIdHandler: GET")

    def put(self, answer_id):
        self.write("QuestionByIdHandler: PUT")

    def delete(self, answer_id):
        self.write("QuestionByIdHandler: DELETE")
