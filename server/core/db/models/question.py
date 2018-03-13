from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import relationship

from core.db.models import LogEntity


class Question(LogEntity):

    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)

    answers = relationship('Answer', cascade='all, delete-orphan')
    tags = relationship('Tag')

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', backref='questions')

    def to_dict(self):
        my_dict = LogEntity.to_dict(self)
        my_dict.update({
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'user': self.user.to_dict()
        })
        return my_dict
