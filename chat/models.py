from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, func


base = declarative_base()


class User(base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created = Column(DateTime, default=func.now())
    messages = relationship("Message")

    def __repr__(self):
        return "<User(email='%s', created='%s')>" % \
               (self.email, self.created)

    @classmethod
    def find_by_email(cls, session, email):
        return session.query(cls).filter(cls.email == email).one_or_none()

    def __json__(self):
        return {
            'id': self.id,
            'email': self.email,
            'created': self.created,
        }


class Message(base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User")
    text = Column(Text)
    created = Column(DateTime, default=func.now())
    modified = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return "<Message(user_id='%s', text='%s', created='%s')>" % \
               (self.user_id, self.text, self.created)

    def __json__(self):
        return {
            'id': self.id,
            'user': self.user,
            'text': self.text,
            'created': self.created,
        }
