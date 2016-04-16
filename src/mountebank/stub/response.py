from collections import namedtuple


undefined = type('_Sentinel', (object,), {})


class http_response(object):
    Mode = namedtuple('Mode', 'BINARY TEXT')('binary', 'text')

    MAPPINGS = {'status_code': 'statusCode',
                'mode': '_mode'}

    __slots__ = ['status_code', 'headers', 'body', 'mode']

    def __init__(self, status_code, headers=undefined,
                 body=undefined, mode=undefined):
        self.status_code = status_code
        self.headers = headers
        self.body = body
        self.mode = mode

    @property
    def json(self):
        result = {}
        for field in self.__slots__:
            value = getattr(self, field)
            if value is not undefined:
                json_field = self.MAPPINGS.get(field, field)
                result[json_field] = value
        return result


class tcp_response(object):
    def __init__(self, data):
        self.data = data

    @property
    def json(self):
        return {'data': self.data}


class ResponseBuilder(object):
    def __init__(self, responses, stub_builder):
        self._responses = responses
        self._stub_builder = stub_builder

    def is_(self, *responses):
        self._responses.extend(
            [{'is': response.json} for response in responses])
        return self._stub_builder

    def proxy(self, response):
        raise NotImplementedError()
