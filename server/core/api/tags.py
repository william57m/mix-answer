from core.api import BaseRequestHandler


class TagHandler(BaseRequestHandler):

    async def get(self):
        self.write("TagHandler: GET")

    async def post(self):
        self.write("TagHandler: POST")


class TagByIdHandler(BaseRequestHandler):

    async def get(self, answer_id):
        self.write("TagByIdHandler: GET")

    async def put(self, answer_id):
        self.write("TagByIdHandler: PUT")

    async def delete(self, answer_id):
        self.write("TagByIdHandler: DELETE")
