import requests


class Imposter(object):
    """Mountebank Imposter API Client

    This class communicates with Mountebank Imposter's public API
    through Python
    """

    def __init__(self, imposter_url):
        self._imposter_url = imposter_url

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
        endpoint = '{}/imposters'.format(self._imposter_url)
        response = requests.post(endpoint, json={
            'name': service_name,
            'port': port, 'protocol': protocol,
        })
        response.raise_for_status()

    def get_by_port(self, port):
        """Get the imposter created at the specified port

        :param port: The port number
        """
        endpoint = '{}/imposters/{}'.format(self._imposter_url, port)
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()


class StubbedService(object):
    """Represents a stubbed service on Mountebank imposter

    """
    pass
