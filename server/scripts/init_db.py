import argparse
import logging
import sys

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from core.db.models import Answer
from core.db.models import Base
from core.db.models import Question
from core.db.models import User
from core.db.models import Vote

from core.utils.config import parse_config

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def main(argv=sys.argv):

    # Parse arguments
    parser = argparse.ArgumentParser(description='Init DB')
    parser.add_argument('-c', '--config', dest='config', required=True)
    parser.add_argument('-t', '--data_test', dest='data_test', required=False, default=False)
    args = parser.parse_args()
    if not args.config:
        parser.print_help()
        sys.exit(1)

    # Get config
    config = parse_config(args.config)

    # Drop db
    engine = create_engine_db(config)
    Base.metadata.drop_all(engine)

    # Init DB
    db = initdb(config)

    # Add data test
    if args.data_test in ['true', True, 1]:
        add_data_test(db)


def drop_db(config):
    db_engine = create_engine_db(config)
    db = scoped_session(sessionmaker(bind=db_engine, autoflush=True))
    db.drop_all()


def create_engine_db(config):
    db_url = config.get('sqlalchemy', 'url')
    return create_engine(db_url, echo=True)


def initdb(config):
    db_engine = create_engine_db(config)

    try:
        logging.info('Creating the database schema')
        Base.metadata.create_all(db_engine)
    except OperationalError as e:
        logging.exception('Unable to connect to the database')
    else:
        logging.info('Successfully initialized the database')
    
    return scoped_session(sessionmaker(bind=db_engine, autoflush=True))


def add_data_test(db):

    # Add users
    u1 = User(firstname="Fernando", lastname="Alonso", email="fernando.alonso@mclaren.com")
    u2 = User(firstname="Kimi", lastname="Raikkonen", email="kimi.raikkonen@ferrari.it")
    db.add(u1)
    db.add(u2)

    # Add answers
    a1 = Answer(message='Message 1', user=u2)
    a2 = Answer(message='Message 2', user=u2)
    a3 = Answer(message='Message 3', user=u1)
    db.add(a1)
    db.add(a2)
    db.add(a3)
    db.flush()

    # Add questions
    db.add(Question(title='Title1', body='Body1', user_id=u1.id, answers=[a1, a2]))
    db.add(Question(title='Title2', body='Body2', user_id=u1.id, answers=[a3]))
    db.add(Question(title='Title3', body='Body3', user_id=u2.id, answers=[]))

    # Add votes
    v1 = Vote(answer_id=a1.id, user_id=u1.id)
    v2 = Vote(answer_id=a1.id, user_id=u2.id)
    db.add(v1)
    db.add(v2)

    # Commit data
    db.commit()


if __name__ == '__main__':
    main()
