from core.api import BaseRequestHandler


class InitHandler(BaseRequestHandler):

    async def get(self):
        ret = {}

        if self.user:
            ret['user'] = self.user.to_dict()

        self.write(ret)
        self.finish()
