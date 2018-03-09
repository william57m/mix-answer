from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String


class Question():

    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    message = Column(String, nullable=False)

    def to_dict(self):

        return {
            'id': self.id,
            'title': self.title,
            'message': self.message
        }
