import json

from sqlalchemy.exc import SQLAlchemyError

from core.api import BaseRequestHandler
from core.db.models import Answer
from core.db.models import Vote
from core.services.authentication import AuthenticationService
from core.utils.exceptions import InternalServerError
from core.utils.query import check_param


class VoteHandler(BaseRequestHandler):

    def prepare(self):
        super().prepare()
        if self.request.method != 'OPTIONS':
            answer_id = self.path_kwargs['answer_id']
            self.answer = self.get_object_by_id(Answer, answer_id)

    @AuthenticationService.requires_login
    async def post(self, answer_id):

        # Get user id
        user_id = self.user.id

        # Create data
        data = json.loads(self.request.body.decode('utf-8'))
        up_down = check_param(data, name='up_down', type_param='boolean', required=True)

        # Check vote
        vote = self.application.db.query(Vote).filter(Vote.answer_id == answer_id) \
                                              .filter(Vote.user_id == user_id) \
                                              .first()

        # Commit in DB
        try:
            if vote and vote.up_down == up_down:
                self.application.db.delete(vote)
            else:
                vote = Vote(user_id=user_id, answer_id=answer_id, up_down=up_down)
                self.application.db.add(vote)
            self.application.db.commit()
        except SQLAlchemyError as error:
            self.application.db.rollback()
            raise InternalServerError('Unable to toggle the vote.', error)

        # Returns response
        self.set_status(201)
        self.finish()
