from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from core.db.models import LogEntity


class Post(LogEntity):

    __abstract__ = True

    id = Column(Integer, primary_key=True)
    body = Column(String, nullable=False)

    # Updated on GET /questions/id
    view_counter = Column(Integer, default=0)

    # Updated on POST /post/id/votes
    vote_counter = Column(Integer, default=0)

    def to_dict(self):
        my_dict = LogEntity.to_dict(self)
        my_dict.update({
            'id': self.id,
            'body': self.body,
            'votes': self.vote_counter,
            'view': self.view_counter
        })
        return my_dict
