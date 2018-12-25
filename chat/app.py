import falcon
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from .config import STORAGES
from .errors import AppError
from .middleware import AuthMiddleware, SQLAlchemySessionManager, RequireJSON
from .resources import user, message

options = {
    'pool_recycle': 3600,
    'pool_size': 10,
    'pool_timeout': 30,
    'max_overflow': 30,
    'echo': True,
    'execution_options': {
        'autocommit': True
    }
}

engine = create_engine(
    '{}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}'.format(
        'postgres',
        **STORAGES['postgres'],
    ),
    **options
)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


app = falcon.API(middleware=[
    AuthMiddleware(),
    SQLAlchemySessionManager(Session),
    RequireJSON(),
])

app.add_error_handler(AppError, AppError.handle)

app.add_route('/api/users', user.Collection())
app.add_route('/api/users/signin', user.Signin())
app.add_route('/api/messages', message.Collection())
