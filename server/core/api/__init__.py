import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound

from tornado.web import RequestHandler
from core.utils.exceptions import ServerHTTPError
from core.utils.exceptions import NotFoundError

log = logging.getLogger(__name__)


class BaseRequestHandler(RequestHandler):

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