from tornado.web import RequestHandler


class TagHandler(RequestHandler):

    def get(self):
        self.write("TagHandler: GET")

    def post(self):
        self.write("TagHandler: POST")


class TagByIdHandler(RequestHandler):

    def get(self, answer_id):
        self.write("TagByIdHandler: GET")

    def put(self, answer_id):
        self.write("TagByIdHandler: PUT")

    def delete(self, answer_id):
        self.write("TagByIdHandler: DELETE")
