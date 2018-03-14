import json

from core.api import BaseRequestHandler
from core.utils.exceptions import BadRequestError
from core.services.authentication import AuthenticationService


class LoginHandler(BaseRequestHandler):

    async def post(self):

        # Authentication service
        authentication_service = AuthenticationService(self)

        # Get data
        data = json.loads(self.request.body.decode('utf-8'))

        # Check params
        if 'email' not in data:
            raise BadRequestError(f'Param email is missing')
        if 'password' not in data:
            raise BadRequestError(f'Param password is missing')

        # Get email and password
        email = data['email'].lower()
        password = data['password']

        # Try to login
        user = await authentication_service.login(email, password)
        if user:
            status = 200
            ret = user.to_dict()
        else:
            status = 401
            ret = {
                'error': {
                    'message': 'Invalid credentials'
                }
            }

        self.set_status(status)
        self.write(ret)
        self.finish()
