from sqlalchemy.exc import SQLAlchemyError

from core.api import BaseRequestHandler
from core.db.models import Answer
from core.db.models import Vote
from core.utils.exceptions import InternalServerError


class VoteHandler(BaseRequestHandler):

    def prepare(self):
        super().prepare()
        if self.request.method != 'OPTIONS':
            answer_id = self.path_kwargs['answer_id']
            self.answer = self.get_object_by_id(Answer, answer_id)

    async def post(self, answer_id):

        # Get user id
        # TODO: take the real user id when the authentication system is ready
        user_id = 1

        # Check vote
        vote = self.application.db.query(Vote).filter(Vote.answer_id == answer_id) \
                                              .filter(Vote.user_id == user_id) \
                                              .first()

        # Commit in DB
        try:
            if vote:
                self.application.db.delete(vote)
            else:
                vote = Vote(user_id=user_id, answer_id=answer_id)
                self.application.db.add(vote)
            self.application.db.commit()
        except SQLAlchemyError as error:
            self.application.db.rollback()
            raise InternalServerError('Unable to toggle the vote.', error)

        # Returns response
        self.set_status(201)
        self.finish()
