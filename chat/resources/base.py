import json
import falcon
from ..utils import AlchemyEncoder


class BaseResource:

    def to_json(self, body_dict):
        return json.dumps(body_dict, cls=AlchemyEncoder, sort_keys=True)

    def on_error(self, res, error=None):
        res.status = error['status']
        meta = dict()
        meta['code'] = error['code']
        meta['message'] = error['message']

        obj = dict()
        obj['meta'] = meta
        res.body = self.to_json(obj)

    def on_success(self, res, data=None):
        res.status = falcon.HTTP_200
        meta = dict()
        meta['code'] = 200
        meta['message'] = 'OK'

        obj = dict()
        obj['meta'] = meta
        obj['data'] = data
        res.body = self.to_json(obj)
