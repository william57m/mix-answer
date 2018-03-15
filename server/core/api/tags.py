from core.api import BaseRequestHandler


class TagHandler(BaseRequestHandler):

    async def get(self):
        self.write("TagHandler: GET")
