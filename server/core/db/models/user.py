from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from core.db.models import Base


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String(500), nullable=True)
    is_admin = Column(Boolean, default=False)


    def to_dict(self):

        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'is_admin': self.is_admin
        }
