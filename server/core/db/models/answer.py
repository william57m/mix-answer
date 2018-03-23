from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer

from sqlalchemy.orm import relationship

from sqlalchemy_utils.types import TSVectorType

from core.db.models import Post


class Answer(Post):

    __tablename__ = 'answers'

    question_id = Column(Integer, ForeignKey('questions.id'))
    question = relationship('Question')

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', backref='answers')

    # Search vector
    search_vector = Column(TSVectorType('body'))

    def to_dict(self):
        my_dict = Post.to_dict(self)
        my_dict.update({
            'question_id': self.question_id,
            'user': self.user.to_dict()
        })
        return my_dict
