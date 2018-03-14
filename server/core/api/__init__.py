import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound

from tornado.web import RequestHandler
from core.db.models import User
from core.utils.exceptions import ServerHTTPError
from core.utils.exceptions import NotFoundError

log = logging.getLogger(__name__)


class BaseRequestHandler(RequestHandler):

    def prepare(self):
        super().prepare()
        self.application.session_store.get(self)

    def get_object_by_id(self, model, obj_id):
        try:
            return self.application.db.query(model)\
                          .filter_by(id=int(obj_id))\
                          .one()
        except NoResultFound:
            raise NotFoundError("No {0} with id {1}".format(model.__name__, obj_id))

    def _handle_request_exception(self, e):
        if isinstance(e, ServerHTTPError):
            if e.error_to_log:
                log.error(e.error_to_log)
            self.set_status(e.status_code)
            self.write(e.payload)
            self.finish()
        elif isinstance(e, SQLAlchemyError):
            self.db.rollback()
            super()._handle_request_exception(e)
        else:
            super()._handle_request_exception(e)

    @property
    def session(self):
        if hasattr(self, '__session__'):
            if self.__session__:
                return self.__session__
        ret = self.application.session_store.get(self)
        self.__session__ = ret
        return ret

    @property
    def user(self):
        if self.session:
            user_id = self.session.user_id
            # If the user exists..
            if user_id is not None:
                return self.application.db.query(User).filter_by(id=user_id).one()
        return None
