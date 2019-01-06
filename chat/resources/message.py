import falcon
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.exc import NoResultFound
from .base import BaseResource
from ..models import Message, User
from ..errors import MessageNotExistsError, UserNotExistsError
from ..hooks import auth_required


class Collection(BaseResource):

    def on_get(self, req, res):
        messages = self.session\
            .query(Message)\
            .options(joinedload('user'))\
            .order_by(Message.created)\
            .all()

        if messages:
            obj = [message.__json__() for message in messages]
            self.on_success(res, obj)
        else:
            raise MessageNotExistsError("It seems that there are no messages in the DB yet")

    @falcon.before(auth_required)
    def on_post(self, req, res):
        data = req.media
        try:
            self.session\
                .query(User)\
                .filter(User.id == req.context['auth_user']['id'])\
                .one()
        except NoResultFound:
            raise UserNotExistsError("Your user is not in the DB.")

        message = Message(
            text=data["text"],
            user_id=req.context['auth_user']['id']
        )

        self.session.add(message)
        self.session.commit()
        self.on_success(res, None)

