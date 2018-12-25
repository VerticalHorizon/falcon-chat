from .models import *
from .app import engine


base.metadata.create_all(engine)
