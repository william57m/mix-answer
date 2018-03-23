from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table

from sqlalchemy.orm import relationship

from sqlalchemy_utils.types import TSVectorType

from core.db.models import Base
from core.db.models import Post


association_table = Table(
    'question__tag', Base.metadata,
    Column('question_id', Integer, ForeignKey('questions.id')),
    Column('tag_id', String, ForeignKey('tags.label', ondelete="CASCADE"))
)


class Question(Post):

    __tablename__ = 'questions'

    title = Column(String, nullable=False)

    answers = relationship('Answer', cascade='all, delete-orphan')
    tags = relationship('Tag', secondary=association_table, backref='questions')

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', backref='questions')

    # Search vector
    search_vector = Column(TSVectorType('title', 'body'))

    def to_dict(self):
        my_dict = Post.to_dict(self)
        my_dict.update({
            'title': self.title,
            'nb_answers': len(self.answers),
            'tags': [tag.label for tag in self.tags],
            'user': self.user.to_dict()
        })
        return my_dict
