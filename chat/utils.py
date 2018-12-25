import json
import datetime
from sqlalchemy.ext.declarative import DeclarativeMeta


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            return obj.__json__()

        elif isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()

        return super().default(self, obj)
