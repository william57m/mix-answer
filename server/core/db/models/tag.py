from sqlalchemy import Column
from sqlalchemy import String

from sqlalchemy_utils.types import TSVectorType

from core.db.models import Base


class Tag(Base):

    __tablename__ = 'tags'

    label = Column(String(25), primary_key=True, nullable=False)

    # Search vector
    search_vector = Column(TSVectorType('label'))

    def to_dict(self):

        return {
            'label': self.label
        }
