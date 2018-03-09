from tornado.web import HTTPError


class ServerHTTPError(HTTPError):
    def __init__(self, status_code, message=None, error_to_log=None, *args, **kwargs):
        super().__init__(status_code, log_message=message, *args, **kwargs)
        self.message = message
        self.error_to_log = error_to_log

    @property
    def payload(self):
        return {
            'error': {
                'message': self.message,
            },
        }


class InternalServerError(ServerHTTPError):
    def __init__(self, *args, **kwargs):
        super().__init__(500, *args, **kwargs)


class BadRequestError(ServerHTTPError):
    def __init__(self, *args, **kwargs):
        super().__init__(400, *args, **kwargs)


class NotFoundError(ServerHTTPError):
    def __init__(self, *args, **kwargs):
        super().__init__(404, *args, **kwargs)


class AuthError(ServerHTTPError):

    reason = "Unauthenticated"
    error_code = 401

    def __init__(self, *args, **kwargs):
        super().__init__(self.__class__.error_code, *args, **kwargs)

    @property
    def payload(self):
        return {
            'code': self.__class__.error_code,
            'status': 'error',
            'reason': self.__class__.reason
        }


class MethodNotAllowedError(ServerHTTPError):

    reason = "Method Not Allowed"
    error_code = 405

    def __init__(self, *args, **kwargs):
        super().__init__(self.__class__.error_code, *args, **kwargs)

    @property
    def payload(self):
        return {
            'code': self.__class__.error_code,
            'status': 'error',
            'reason': self.__class__.reason
        }
