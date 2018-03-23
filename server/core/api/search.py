import json

from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy_searchable import search

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


class SearchHandler(BaseRequestHandler):

    async def get(self):

        # Prepare query
        query = self.application.db.query(Question)

        # Search
        search_value = self.get_argument('q', False)
        if search_value:
            query = search(query, search_value)

        # Sort and limit
        metadata = extract_metadata(query)
        query = order_query(self, query)
        query = limit_offset_query(self, query, metadata)

        # Get questions
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
