from sqlalchemy import Column
from sqlalchemy import String

from core.db.models import Base


class Tag(Base):

    __tablename__ = 'tags'

    label = Column(String(25), primary_key=True, nullable=False)

    def to_dict(self):

        return {
            'label': self.label
        }
