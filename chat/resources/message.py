import falcon
from sqlalchemy.orm import lazyload
from .base import BaseResource
from ..models import Message
from ..errors import AppError
from ..hooks import auth_required


class Collection(BaseResource):

    def on_get(self, req, res):
        messages = self.session\
            .query(Message)\
            .options(lazyload('user'))\
            .order_by(Message.created)\
            .all()

        if messages:
            obj = [message.__json__() for message in messages]
            self.on_success(res, obj)
        else:
            raise AppError(description="No messages found!")

    @falcon.before(auth_required)
    def on_post(self, req, res):
        data = req.media
        message = Message(
            text=data["text"],
            user_id=req.context['auth_user']['id']
        )

        self.session.add(message)
        self.session.commit()
        self.on_success(res, None)

