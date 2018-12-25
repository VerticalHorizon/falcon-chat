import jwt
from .errors import NotSupportedError
from .config import SECRET_KEY


class AuthMiddleware:

    def process_request(self, req, resp):
        header = req.get_header('Authorization')

        if header is not None:
            token = header.split(' ')[-1]
            req.context['auth_user'] = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        else:
            req.context['auth_user'] = None


class SQLAlchemySessionManager:
    """
    Create a scoped session for every request and close it when the request
    ends.
    """

    def __init__(self, session):
        self.session = session

    def process_resource(self, req, resp, resource, params):
        resource.session = self.session()

    def process_response(self, req, resp, resource, req_succeeded):
        if hasattr(resource, 'session'):
            if not req_succeeded:
                resource.session.rollback()
            self.session.remove()


class RequireJSON:

    def process_request(self, req, resp):
        if not req.client_accepts_json:
            raise NotSupportedError(description='This API only supports responses encoded as JSON.')

        if req.method in ('POST', 'PUT'):
            if 'application/json' not in req.content_type:
                raise NotSupportedError(description='This API only supports requests encoded as JSON.')
