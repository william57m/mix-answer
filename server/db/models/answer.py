from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String


class Answer():

    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True)
    message = Column(String, nullable=False)

    def to_dict(self):

        return {
            'id': self.id,
            'message': self.message
        }
