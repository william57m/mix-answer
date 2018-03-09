from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String


class Tag():

    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    label = Column(String(25), nullable=False)

    def to_dict(self):

        return {
            'id': self.id,
            'label': self.label
        }
