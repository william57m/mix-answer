import json
import hashlib

from sqlalchemy.exc import SQLAlchemyError

from core.api import BaseRequestHandler
from core.db.models import User
from core.utils.exceptions import InternalServerError
from core.utils.query import check_param
from core.utils.query import extract_metadata
from core.utils.query import limit_offset_query
from core.utils.query import order_query


class UserHandler(BaseRequestHandler):

    async def post(self):
        # Create data
        data = json.loads(self.request.body.decode('utf-8'))
        firstname = check_param(data, name='firstname', type_param='string', required=True)
        lastname = check_param(data, name='lastname', type_param='string', required=True)
        email = check_param(data, name='email', type_param='email', required=True)
        password = check_param(data, name='password', type_param='string', required=True)
        hashed_password = hashlib.md5(password.encode('utf-8')).hexdigest()

        user = User(firstname=firstname, lastname=lastname, email=email.lower(), password=hashed_password)
        self.application.db.add(user)

        # Commit in DB
        try:
            self.application.db.commit()
        except SQLAlchemyError as error:
            self.application.db.rollback()
            raise InternalServerError('Unable to create the user.', error)

        # Returns response
        self.set_status(201)
        self.write({'data': user.to_dict()})
        self.finish()
