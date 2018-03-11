from core.api import BaseRequestHandler


class AnswerHandler(BaseRequestHandler):

    async def get(self):
        self.write("AnswerHandler: GET")

    async def post(self):
        self.write("AnswerHandler: POST")


class AnswerByIdHandler(BaseRequestHandler):

    async def get(self, answer_id):
        self.write("AnswerByIdHandler: GET")

    async def put(self, answer_id):
        self.write("AnswerByIdHandler: PUT")

    async def delete(self, answer_id):
        self.write("AnswerByIdHandler: DELETE")
