import requests
from mountebank import exceptions
from collections import namedtuple


class _Sentinel(object):
    pass


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
                result[json_field] = self.status_code
        return result

class StubBuilder(object):
    def __init__(self):
        self._responses = []
        self._predicates = []

    @property
    def response(self):
        return ResponseBuilder(self._responses)

    def build(self):
        assert self._responses
        stub = {
            'responses': self._responses,
        }
        if self._predicates:
            stub['predicates'] = self._predicates
        return stub


class ResponseBuilder(object):
    def __init__(self, responses):
        self._responses = responses

    def is_(self, response):
        self._responses.append({
            'is': response.json
        })
        return self


class Imposter(object):
    """Mountebank Imposter API Client

    This class communicates with Mountebank Imposter's public API
    through Python
    """

    def __init__(self, imposter_url):
        self._imposter_url = imposter_url

    @staticmethod
    def _raise_if_status_is_not(response, *expected_status_codes):
        if response.status_code not in expected_status_codes:
            raise exceptions.ImposterException(response)

    def create(self, service_name, protocol, port, **specs):
        """Create a stubbed service in mountebank

        :param service_name: The name of the service
        :param protocol: The protocol of the service.
                         It has to be one of the protocols
                         that mountebank supports,
                         e.g., http, https, tcp, smtp
        :param port: The port of the service
        :param specs: The specs the stubbed service should run on
        """
        response = requests.post(self._imposter_url, json={
            'name': service_name,
            'port': port, 'protocol': protocol,
        })
        self._raise_if_status_is_not(response, 201)
        return response

    def get_by_port(self, port):
        """Get the imposter created at the specified port

        :param port: The port number
        """
        endpoint = '{}/{}'.format(self._imposter_url, port)
        response = requests.get(endpoint)
        self._raise_if_status_is_not(response, 200)
        return response.json()

    def delete(self, port):
        """Delete the imposter created at the specified port

        :param port: The port number
        """
        endpoint = '{}/{}'.format(self._imposter_url, port)
        response = requests.delete(endpoint)
        self._raise_if_status_is_not(response, 200)
        return response.json()


class StubbedService(object):
    """Represents a stubbed service on Mountebank imposter

    """
    pass
