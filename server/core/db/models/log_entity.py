from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer

from core.db.models import Base
from core.utils import date


class LogEntity(Base):

    __abstract__ = True

    creator_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        my_dict = dict()

        my_dict['creator_id'] = self.creator_id
        my_dict['created_at'] = date.format_datetime_object(self.created_at)
        my_dict['last_updated'] = date.format_datetime_object(self.last_updated)

        return my_dict
