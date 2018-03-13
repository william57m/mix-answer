import json

from sqlalchemy.exc import SQLAlchemyError

from core.api import BaseRequestHandler
from core.db.models import Question
from core.utils.exceptions import InternalServerError
from core.utils.query import check_param
from core.utils.query import extract_metadata
from core.utils.query import limit_offset_query
from core.utils.query import order_query
from core.utils.query import update_by_property_list


class QuestionHandler(BaseRequestHandler):

    async def get(self):

        # Prepare query
        query = self.application.db.query(Question)
        metadata = extract_metadata(query)
        query = order_query(self, query)
        query = limit_offset_query(self, query, metadata)
        questions = query.all()

        # Prepare data to return
        ret = {
            'data': [question.to_dict() for question in questions],
            'metadata': metadata
        }

        # Returns response
        self.set_status(200)
        self.write(ret)
        self.finish()

    async def post(self):

        # Get user from cookie
        from core.db.models import User
        current_user = User(firstname='1', lastname='2', email='3')
        self.application.db.add(current_user)

        # Create data
        data = json.loads(self.request.body.decode('utf-8'))
        title = check_param(data, name='title', type='string', required=True)
        body = check_param(data, name='body', type='string', required=True)
        question = Question(title=title, body=body, user=current_user)

        # Commit in DB
        try:
            self.application.db.add(question)
            self.application.db.commit()
        except SQLAlchemyError as error:
            self.application.db.rollback()
            raise InternalServerError('Unable to create the question.', error)

        # Returns response
        self.set_status(201)
        self.write({'data': question.to_dict()})
        self.finish()


class QuestionByIdHandler(BaseRequestHandler):

    def prepare(self):
        super().prepare()
        if self.request.method != 'OPTIONS':
            question_id = self.path_kwargs['question_id']
            self.question = self.get_object_by_id(Question, question_id)

    async def put(self, question_id):

        # Update basic properties
        data = json.loads(self.request.body.decode('utf-8'))
        update_by_property_list(['title', 'body'], data, self.question)

        # Commit in DB
        try:
            self.application.db.commit()
        except SQLAlchemyError as error:
            self.application.db.rollback()
            raise InternalServerError('Unable to update the question.', error)

        # Returns response
        self.set_status(200)
        self.write({'data': self.question.to_dict()})
        self.finish()

    async def delete(self, question_id):
        try:
            self.application.db.delete(self.question)
            self.application.db.commit()
        except SQLAlchemyError as error:
            self.application.db.rollback()
            raise InternalServerError('Unable to delete the question.', error)

        self.set_status(204)
        self.finish()
