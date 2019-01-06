import falcon
from cerberus import Validator
from passlib.hash import pbkdf2_sha256
import jwt
from .base import BaseResource
from ..models import User
from ..errors import PasswordNotMatch, InvalidParameterError, UserNotExistsError
from ..config import SECRET_KEY


FIELDS = {
    'email': {
        'type': 'string',
        'regex': '[a-zA-Z0-9._-]+@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,4}',
        'required': True,
        'maxlength': 255
    },
    'password': {
        'type': 'string',
        'regex': '[0-9a-zA-Z]\w{3,14}',
        'required': True,
        'minlength': 8,
        'maxlength': 64
    },
}


def validate_user(req, res, resource, params):
    schema = {
        'email': FIELDS['email'],
        'password': FIELDS['password'],
    }

    v = Validator(schema)
    if not v.validate(req.media):
        raise InvalidParameterError(v.errors)


class Collection(BaseResource):
    """
    Handle for endpoint: /api/users/
    """
    def on_get(self, req, res):
        user_dbs = self.session.query(User).all()
        if user_dbs:
            obj = [user.__json__() for user in user_dbs]
            self.on_success(res, obj)
        else:
            raise UserNotExistsError("It seems that there are no users in DB yet.")


class Signin(BaseResource):
    """
    Handle for endpoint: /api/users/signin
    Signin & auto signup
    """
    @falcon.before(validate_user)
    def on_post(self, req, res):
        data = req.media
        email = data['email']
        password = data['password']

        user_db = User.find_by_email(self.session, email)

        if user_db:
            if pbkdf2_sha256.verify(password, user_db.password.encode('utf-8')):
                payload = {
                    "id": user_db.id,
                    "email": user_db.email,
                }
                self.on_success(res, jwt.encode(payload, SECRET_KEY).decode('utf-8'))
            else:
                raise PasswordNotMatch()
        else:
            user = User()
            user.email = email
            user.password = pbkdf2_sha256.encrypt(password, rounds=80000, salt_size=100)

            self.session.add(user)
            self.session.commit()

            payload = {
                "id": user.id,
                "email": user.email,
            }
            self.on_success(res, jwt.encode(payload, SECRET_KEY).decode('utf-8'))
