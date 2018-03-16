from core.api import BaseRequestHandler
from core.db.models import Tag
from core.utils.query import extract_metadata
from core.utils.query import limit_offset_query
from core.utils.query import order_query


class TagHandler(BaseRequestHandler):

    async def get(self):

        # Prepare query
        query = self.application.db.query(Tag)
        metadata = extract_metadata(query)
        query = order_query(self, query)
        query = limit_offset_query(self, query, metadata)
        tags = query.all()

        # Prepare data to return
        ret = {
            'data': [tag.to_dict() for tag in tags],
            'metadata': metadata
        }

        # Returns response
        self.set_status(200)
        self.write(ret)
        self.finish()
