import json

from sqlalchemy.exc import SQLAlchemyError

from core.api import BaseRequestHandler
from core.db.models import Answer
from core.db.models import Question
from core.db.models import VoteAnswer
from core.db.models import VoteQuestion
from core.services.authentication import AuthenticationService
from core.utils.exceptions import InternalServerError
from core.utils.query import check_param


class VoteHandler(BaseRequestHandler):

    def get_data(self):
        data = json.loads(self.request.body.decode('utf-8'))
        up_down = check_param(data, name='up_down', type_param='boolean', required=True)
        return up_down

    def get_vote(self, kind, id):
        # Get user id
        user_id = self.user.id

        # Prepare query                               
        if kind == 'answer':
            query = self.application.db.query(VoteAnswer).filter(VoteAnswer.user_id == user_id)
            query = query.filter(VoteAnswer.answer_id == id)
        else:
            query = self.application.db.query(VoteQuestion).filter(VoteQuestion.user_id == user_id)
            query = query.filter(VoteQuestion.question_id == id)

        return query.first()

    def get_count_offset(self, vote, up_down):
        value = 0
        if vote and vote.up_down == up_down:
            value = -1 if vote.up_down else 1
        elif vote:
            value = 2 if up_down else -2
        else:
            value = 1 if up_down else -1
        return value

    def update_vote(self, kind, id, vote, up_down):
        # Get user id
        user_id = self.user.id

        if vote and vote.up_down == up_down:
            self.application.db.delete(vote)
        elif vote:
            vote.up_down = up_down
        else:
            if kind == 'answer':
                vote = VoteAnswer(user_id=user_id, answer_id=id, up_down=up_down)
            else:
                vote = VoteQuestion(user_id=user_id, question_id=id, up_down=up_down)
            self.application.db.add(vote)


class AnswerVoteHandler(VoteHandler):

    def prepare(self):
        super().prepare()
        if self.request.method != 'OPTIONS':
            answer_id = self.path_kwargs['answer_id']
            self.answer = self.get_object_by_id(Answer, answer_id)

    @AuthenticationService.requires_login
    async def post(self, answer_id):

        # Get data
        up_down = self.get_data()
        vote = self.get_vote('answer', answer_id)

        # Commit in DB
        try:
            # Update count
            value = self.get_count_offset(vote, up_down)
            self.update_vote('answer', answer_id, vote, up_down)
            self.answer.vote_counter = self.answer.vote_counter + value
            self.application.db.commit()
        except SQLAlchemyError as error:
            self.application.db.rollback()
            raise InternalServerError('Unable to toggle the vote.', error)

        # Returns response
        self.set_status(201)
        self.finish()


class QuestionVoteHandler(VoteHandler):

    def prepare(self):
        super().prepare()
        if self.request.method != 'OPTIONS':
            question_id = self.path_kwargs['question_id']
            self.question = self.get_object_by_id(Question, question_id)

    @AuthenticationService.requires_login
    async def post(self, question_id):

        # Get data
        up_down = self.get_data()
        vote = self.get_vote('question', question_id)

        # Commit in DB
        try:
            # Update count
            value = self.get_count_offset(vote, up_down)
            self.update_vote('question', question_id, vote, up_down)
            self.question.vote_counter = self.question.vote_counter + value
            self.application.db.commit()
        except SQLAlchemyError as error:
            self.application.db.rollback()
            raise InternalServerError('Unable to toggle the vote.', error)

        # Returns response
        self.set_status(201)
        self.finish()
