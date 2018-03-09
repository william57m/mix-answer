from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import relationship

from core.db.models import Base


class Tag(Base):

    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    label = Column(String(25), nullable=False)
    question_id = Column(Integer, ForeignKey('questions.id'))
    question = relationship("Question")

    def to_dict(self):

        return {
            'id': self.id,
            'label': self.label,
            'question_id': self.question_id
        }
