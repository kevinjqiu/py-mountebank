import requests
from mountebank import exceptions
from mountebank.stub.builder import StubBuilder


class MountebankClient(object):
    def __init__(self, mountebank_url):
        self._mountebank_url = mountebank_url

    @property
    def imposter(self):
        return Imposter('{}/imposters'.format(self._mountebank_url))


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

    def create(self, service_name, protocol, port, stubs=None):
        """Create a stubbed service in mountebank

        :param service_name: The name of the service
        :param protocol: The protocol of the service.
                         It has to be one of the protocols
                         that mountebank supports,
                         e.g., http, https, tcp, smtp
        :param port: The port of the service
        :param specs: The specs the stubbed service should run on
        """
        payload = {
            'name': service_name,
            'port': port, 'protocol': protocol,
        }
        if stubs:
            payload['stubs'] = stubs
        response = requests.post(self._imposter_url, json=payload)
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

    def new_stub_builder(self):
        """Returns an instance of StubBuilder
        """
        return StubBuilder()
