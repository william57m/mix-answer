from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_searchable import make_searchable

Base = declarative_base()
make_searchable(Base.metadata)

__all__ = [
    'Answer',
    'Base',
    'LogEntity',
    'Post',
    'Question',
    'Tag',
    'User',
    'VoteAnswer',
    'VoteQuestion'
]

# Model import to expose in core.db.models
from core.db.models.log_entity import LogEntity
from core.db.models.post import Post
from core.db.models.answer import Answer
from core.db.models.question import Question
from core.db.models.tag import Tag
from core.db.models.user import User
from core.db.models.vote import VoteAnswer
from core.db.models.vote import VoteQuestion
