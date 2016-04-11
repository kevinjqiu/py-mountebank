from collections import namedtuple
from mountebank.predicates import PredicateBuilder


class _Sentinel(object):
    """Act as sentinel object
    """


undefined = _Sentinel()


class HTTPResponse(object):
    Mode = namedtuple('Mode', 'BINARY TEXT')('binary', 'text')

    MAPPINGS = {'status_code': 'statusCode',
                'mode': '_mode'}

    __slot__ = ['status_code', 'headers', 'body', 'mode']

    def __init__(self, status_code, headers=undefined,
                 body=undefined, mode=undefined):
        self.status_code = status_code
        self.headers = headers
        self.body = body
        self.mode = mode

    @property
    def json(self):
        result = {}
        for field in ['status_code', 'headers', 'body', 'mode']:
            value = getattr(self, field)
            if value is not undefined:
                json_field = self.MAPPINGS.get(field, field)
                result[json_field] = value
        return result


class ResponseBuilder(object):
    def __init__(self, responses):
        self._responses = responses

    def is_(self, response):
        self._responses.append({
            'is': response.json
        })
        return self

    def proxy(self, response):
        raise NotImplementedError()
