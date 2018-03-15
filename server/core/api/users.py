from core.api import BaseRequestHandler


class UserHandler(BaseRequestHandler):

    async def post(self):
        self.write("UserHandler: POST")
