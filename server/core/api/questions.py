import json

from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

from core.api import BaseRequestHandler
from core.db.models import Answer
from core.db.models import Question
from core.db.models import Tag
from core.services.authentication import AuthenticationService
from core.utils.exceptions import BadRequestError
from core.utils.exceptions import InternalServerError
from core.utils.query import check_param
from core.utils.query import extract_metadata
from core.utils.query import limit_offset_query
from core.utils.query import order_query
from core.utils.query import update_by_property_list

import logging
log = logging.getLogger(__name__)
class QuestionHandler(BaseRequestHandler):

    async def get(self):

        # Prepare query
        query = self.application.db.query(Question)
        if self.get_argument('unanswered', False) == 'true':
            questions_with_answer_id = self.application.db.query(func.distinct(Answer.question_id))
            query = query.filter(Question.id.notin_(questions_with_answer_id))
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

    @AuthenticationService.requires_login
    async def post(self):

        # Create data
        data = json.loads(self.request.body.decode('utf-8'))
        title = check_param(data, name='title', type_param='string', required=True)
        body = check_param(data, name='body', type_param='string', required=True)
        tags = check_param(data, name='tags', type_param='list', required=True)
        if len(tags) < 1:
            raise BadRequestError('At least one tag is required')

        # Add tag
        tags_to_add = []
        for tag_str in tags:
            tag = self.application.db.query(Tag).filter_by(label=tag_str).first()
            if tag is None:
                tag = Tag(label=tag_str)
                self.application.db.add(tag)
            tags_to_add.append(tag)

        question = Question(title=title, body=body, user=self.user, tags=tags_to_add)
        self.application.db.add(question)

        # Commit in DB
        try:
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
            obj_id = self.path_kwargs['question_id']
            self.object = self.get_object_by_id(Question, obj_id)

    async def get(self, question_id):

        # Get answers
        question = self.object.to_dict()
        answers = [answer.to_dict() for answer in self.object.answers]

        # Update view counter in DB
        try:
            # Increment view counter (Naive way)
            # TO IMPROVE
            self.object.view_counter = self.object.view_counter + 1
            self.application.db.commit()
        except SQLAlchemyError as error:
            self.application.db.rollback()
            raise InternalServerError('Unable to create the question.', error)

        # Returns response
        self.set_status(200)
        self.write({'question': question, 'answers': answers})
        self.finish()

    @AuthenticationService.requires_login
    @AuthenticationService.requires_ownership
    async def put(self, question_id):

        # Update basic properties
        data = json.loads(self.request.body.decode('utf-8'))
        update_by_property_list(['title', 'body'], data, self.object)

        # Update tags
        if 'tags' in data:
            tags = check_param(data, name='tags', type_param='list', required=True)
            if len(tags) < 1:
                raise BadRequestError('At least one tag is required')

            # Add tag
            tags_to_add = []
            for tag_str in tags:
                tag = self.application.db.query(Tag).filter_by(label=tag_str).first()
                if tag is None:
                    tag = Tag(label=tag_str)
                    self.application.db.add(tag)
                tags_to_add.append(tag)

            # Update property in question
            self.object.tags = tags_to_add

        # Commit in DB
        try:
            self.application.db.commit()
        except SQLAlchemyError as error:
            self.application.db.rollback()
            raise InternalServerError('Unable to update the question.', error)

        # Returns response
        self.set_status(200)
        self.write({'data': self.object.to_dict()})
        self.finish()

    @AuthenticationService.requires_login
    @AuthenticationService.requires_ownership
    async def delete(self, question_id):
        try:
            self.application.db.delete(self.object)
            self.application.db.commit()
        except SQLAlchemyError as error:
            self.application.db.rollback()
            raise InternalServerError('Unable to delete the question.', error)

        self.set_status(204)
        self.finish()
