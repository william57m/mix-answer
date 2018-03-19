from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer

from sqlalchemy.ext.declarative import declared_attr

from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship

from core.db.models import Base


class Vote(Base):

    __abstract__ = True

    up_down = Column(Boolean, default=True)

    @declared_attr
    def user_id(cls):
        return Column(Integer, ForeignKey('users.id'), nullable=False, primary_key=True)

    @declared_attr
    def user(cls):
        return relationship('User', backref=backref(cls.__backref_name__, cascade='all, delete-orphan'))
     

class VoteAnswer(Vote):

    __tablename__ = 'votes_answers'
    __backref_name__ = 'votes_answers'

    answer_id = Column(Integer, ForeignKey('answers.id'), nullable=False, primary_key=True)
    answer = relationship('Answer', backref=backref('votes', cascade='all, delete-orphan'))


class VoteQuestion(Vote):

    __tablename__ = 'votes_questions'
    __backref_name__ = 'votes_questions'

    question_id = Column(Integer, ForeignKey('questions.id'), nullable=False, primary_key=True)
    question = relationship('Question', backref=backref('votes', cascade='all, delete-orphan'))
