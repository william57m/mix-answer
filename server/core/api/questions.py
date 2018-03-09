from sqlalchemy.exc import SQLAlchemyError
from tornado.web import RequestHandler

from core.db.models import Question
from core.utils.exceptions import InternalServerError
from core.utils.query import check_param
from core.utils.query import extract_metadata
from core.utils.query import limit_offset_query
from core.utils.query import order_query


class QuestionHandler(RequestHandler):

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

        # Create data
        data = self.request_body
        title = check_param(data, name='title', type='string', required=True)
        body = check_param(data, name='body', type='string', required=True)
        question = Question(title=title, body=body)

        # Commit in DB
        try:
            self.db.add(question)
            self.db.commit()
        except SQLAlchemyError as error:
            self.db.rollback()
            raise InternalServerError('Unable to create the question.', error)

        # Returns response
        self.set_status(201)
        self.write({'data': question.to_dict()})
        self.finish()


class QuestionByIdHandler(RequestHandler):

    async def get(self, answer_id):
        self.write("QuestionByIdHandler: GET")

    async def put(self, answer_id):
        self.write("QuestionByIdHandler: PUT")

    async def delete(self, answer_id):
        self.write("QuestionByIdHandler: DELETE")
