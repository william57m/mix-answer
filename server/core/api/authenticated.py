from core.api import BaseRequestHandler
from core.services.authentication import AuthenticationService


class AuthenticatedHandler(BaseRequestHandler):

    @AuthenticationService.requires_login
    async def get(self):
        self.set_status(204)
        self.finish()
