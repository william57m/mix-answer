import json

from sqlalchemy.exc import SQLAlchemyError

from core.api import BaseRequestHandler
from core.db.models import Answer
from core.db.models import Question
from core.services.authentication import AuthenticationService
from core.utils.exceptions import InternalServerError
from core.utils.query import check_param
from core.utils.query import extract_metadata
from core.utils.query import limit_offset_query
from core.utils.query import order_query
from core.utils.query import update_by_property_list


class AnswerHandler(BaseRequestHandler):

    def prepare(self):
        super().prepare()
        if self.request.method != 'OPTIONS':
            question_id = self.path_kwargs['question_id']
            self.question = self.get_object_by_id(Question, question_id)

    async def get(self, question_id):

        # Prepare query
        query = self.application.db.query(Answer).filter(Answer.question_id == question_id)
        metadata = extract_metadata(query)
        query = order_query(self, query)
        query = limit_offset_query(self, query, metadata)
        answers = query.all()

        # Prepare data to return
        ret = {
            'data': [answer.to_dict() for answer in answers],
            'metadata': metadata
        }

        # Returns response
        self.set_status(200)
        self.write(ret)
        self.finish()

    @AuthenticationService.requires_login
    async def post(self, question_id):

        # Create data
        data = json.loads(self.request.body.decode('utf-8'))
        body = check_param(data, name='body', type_param='string', required=True)
        answer = Answer(body=body, question_id=question_id, user=self.user)

        # Commit in DB
        try:
            self.application.db.add(answer)
            self.application.db.commit()
        except SQLAlchemyError as error:
            self.application.db.rollback()
            raise InternalServerError('Unable to create the answer.', error)

        # Returns response
        self.set_status(201)
        self.write({'data': answer.to_dict()})
        self.finish()


class AnswerByIdHandler(BaseRequestHandler):

    def prepare(self):
        super().prepare()
        if self.request.method != 'OPTIONS':
            obj_id = self.path_kwargs['answer_id']
            self.object = self.get_object_by_id(Answer, obj_id)

    @AuthenticationService.requires_login
    @AuthenticationService.requires_ownership
    async def put(self, answer_id):

        # Update basic properties
        data = json.loads(self.request.body.decode('utf-8'))
        update_by_property_list(['body'], data, self.object)

        # Commit in DB
        try:
            self.application.db.commit()
        except SQLAlchemyError as error:
            self.application.db.rollback()
            raise InternalServerError('Unable to update the answer.', error)

        # Returns response
        self.set_status(200)
        self.write({'data': self.object.to_dict()})
        self.finish()

    @AuthenticationService.requires_login
    @AuthenticationService.requires_ownership
    async def delete(self, answer_id):
        try:
            self.application.db.delete(self.object)
            self.application.db.commit()
        except SQLAlchemyError as error:
            self.application.db.rollback()
            raise InternalServerError('Unable to delete the answer.', error)

        self.set_status(204)
        self.finish()
