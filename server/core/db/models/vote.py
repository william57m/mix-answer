from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer

from core.db.models import Base


class Vote(Base):

    __tablename__ = 'votes'

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, primary_key=True)
    answer_id = Column(Integer, ForeignKey('answers.id'), nullable=False, primary_key=True)
