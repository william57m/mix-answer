from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer

from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship

from core.db.models import Base


class Vote(Base):

    __tablename__ = 'votes'

    up_down = Column(Boolean, default=True)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, primary_key=True)
    user = relationship('User', backref=backref('votes', cascade='all, delete-orphan'))

    answer_id = Column(Integer, ForeignKey('answers.id'), nullable=False, primary_key=True)
    answer = relationship('Answer', backref=backref('votes', cascade='all, delete-orphan'))
