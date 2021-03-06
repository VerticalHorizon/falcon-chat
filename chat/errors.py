import json
import falcon


OK = {
    'status': falcon.HTTP_200,
    'code': 200,
}

ERR_UNKNOWN = {
    'status': falcon.HTTP_500,
    'code': 500,
    'title': 'Unknown Error'
}

ERR_AUTH_REQUIRED = {
    'status': falcon.HTTP_401,
    'code': 401,
    'title': 'Authentication Required'
}

ERR_INVALID_PARAMETER = {
    'status': falcon.HTTP_400,
    'code': 400,
    'title': 'Invalid Parameter'
}

ERR_DATABASE_ROLLBACK = {
    'status': falcon.HTTP_500,
    'code': 500,
    'title': 'Database Rollback Error'
}

ERR_NOT_SUPPORTED = {
    'status': falcon.HTTP_404,
    'code': 404,
    'title': 'Not Supported'
}

ERR_USER_NOT_EXISTS = {
    'status': falcon.HTTP_404,
    'code': 404,
    'title': 'User Not Exists'
}

ERR_MESSAGE_NOT_EXISTS = {
    'status': falcon.HTTP_404,
    'code': 404,
    'title': 'Message Not Exists'
}

ERR_PASSWORD_NOT_MATCH = {
    'status': falcon.HTTP_400,
    'code': 400,
    'title': 'Password Not Match'
}


class AppError(Exception):
    def __init__(self, error=ERR_UNKNOWN, description=None):
        self.error = error
        self.error['description'] = description

    @property
    def code(self):
        return self.error['code']

    @property
    def title(self):
        return self.error['title']

    @property
    def status(self):
        return self.error['status']

    @property
    def description(self):
        return self.error['description']

    @staticmethod
    def handle(exception, req, res, error=None):
        res.status = exception.status
        meta = dict()
        meta['code'] = exception.code
        meta['message'] = exception.title
        if exception.description:
            meta['description'] = exception.description
        res.body = json.dumps({'meta': meta})


class InvalidParameterError(AppError):
    def __init__(self, description=None):
        super().__init__(ERR_INVALID_PARAMETER)
        self.error['description'] = description


class DatabaseError(AppError):
    def __init__(self, error, args=None, params=None):
        super().__init__(error)
        obj = dict()
        obj['details'] = ', '.join(args)
        obj['params'] = str(params)
        self.error['description'] = obj


class UserNotExistsError(AppError):
    def __init__(self, description=None):
        super().__init__(ERR_USER_NOT_EXISTS)
        self.error['description'] = description


class MessageNotExistsError(AppError):
    def __init__(self, description=None):
        super().__init__(ERR_MESSAGE_NOT_EXISTS)
        self.error['description'] = description


class PasswordNotMatch(AppError):
    def __init__(self, description=None):
        super().__init__(ERR_PASSWORD_NOT_MATCH)
        self.error['description'] = description


class UnauthorizedError(AppError):
    def __init__(self, description=None):
        super().__init__(ERR_AUTH_REQUIRED)
        self.error['description'] = description


class NotSupportedError(AppError):
    def __init__(self, description=None):
        super().__init__(ERR_NOT_SUPPORTED)
        self.error['description'] = description
