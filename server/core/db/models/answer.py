from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import relationship

from core.db.models import LogEntity


class Answer(LogEntity):

    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True)
    message = Column(String, nullable=False)
    question_id = Column(Integer, ForeignKey('questions.id'))
    question = relationship('Question')

    def to_dict(self):
        my_dict = LogEntity.to_dict(self)
        my_dict.update({
            'id': self.id,
            'message': self.message,
            'question_id': self.question_id
        })
        return my_dict
