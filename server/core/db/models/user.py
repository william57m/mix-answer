import hashlib

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from core.db.models import LogEntity


class User(LogEntity):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String(500), nullable=True)
    is_admin = Column(Boolean, default=False)

    def to_dict(self):
        my_dict = LogEntity.to_dict(self)
        my_dict.update({
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'gravatar_url': self.get_gravatar_thumbnail(),
            'is_admin': self.is_admin
        })
        my_dict.update({
            'nb_answers': len(self.answers)
        })
        return my_dict

    def get_gravatar_thumbnail(self, size=150):
        email = self.email.encode('utf-8')
        gravatar_url = "//www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest()
        gravatar_url = '%s?d=%s&s=%s' % (gravatar_url, 'retro', str(size))
        return gravatar_url
