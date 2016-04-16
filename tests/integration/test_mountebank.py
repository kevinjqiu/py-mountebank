import requests
import pytest
import six

from docker import errors as docker_errors
from mountebank import (
    MountebankClient, ImposterException,
    http_request, http_response,
    tcp_request, tcp_response,
)
from tests.integration import harness


def teardown_module(module):
    harness.stop_mb()


@pytest.fixture()
def socket_factory():
    import socket
    class _SocketFactory(object):
        def __init__(self, host, port):
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.connect((host, port))
            self._socket.settimeout(5)

        def __del__(self):
            self._socket.shutdown()
            self._socket.close()

        def send_and_recv(self, msg):
            self._socket.send(msg)
            return self._socket.recv(255)

    return _SocketFactory


@pytest.fixture(scope='module')
def mb_client():
    mb_url = harness.start_mb(stubbed_ports=[65000])
    assert mb_url is not None
    return MountebankClient(mb_url)


@pytest.fixture(scope='module')
def imposter_client(mb_client):
    return mb_client.imposter


def test_imposter_create(imposter_client):
    imposter_client.create('dummy', 'http', 65000)
    assert_stubbed_service(imposter_client, 65000,
                           expectations={
                               'name': 'dummy',
                               'protocol': 'http',
                               'port': 65000,
                           })


def test_imposter_create_returns_error_if_already_stubbed(imposter_client):
    imposter_client.delete(65000)
    imposter_client.create('dummy', 'http', 65000)
    with pytest.raises(ImposterException) as excinfo:
        imposter_client.create('foobar', 'http', 65000)


def test_imposter_create_with_spec(imposter_client):
    imposter_client.delete(65000)
    stubs = []
    stubs.append(
        imposter_client.new_stub_builder()
        .when(http_request.method == 'POST',
              http_request.path == '/customers/123')
        .response
        .is_(http_response(status_code=201,
                           headers={
                               'Location': 'http://localhost:65000/customers/123',
                               'Content-Type': 'application/xml'},
                           body='<customer><email>customer@test.com</email></customer>'),
             http_response(status_code=400,
                           headers={
                               'Content-Type': 'application/xml'},
                           body='<error>email already exists</error>')
        ).build())
    stubs.append(
        imposter_client.new_stub_builder()
        .response.is_(http_response(status_code=404))
        .build())

    imposter_client.create('sample', 'http', 65000, stubs=stubs)

    response = requests.post('http://localhost:65000/customers/123', data={})
    assert response.status_code == 201
    assert response.headers['Content-Type'] == 'application/xml'
    assert 'customer@test.com' in response.text

    response = requests.post('http://localhost:65000/customers/123', data={})
    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/xml'
    assert 'email already exists' in response.text

    response = requests.get('http://localhost:65000/customers/999')
    assert response.status_code == 404


def test_imposter_with_equals_predicate(imposter_client):
    imposter_client.delete(65000)
    stubs = []
    stubs.append(
        imposter_client.new_stub_builder()
        .when(http_request.method == 'POST',
              http_request.path == '/test',
              http_request.query == {'first': '1', 'second': '2'},
              http_request.headers == {'Accept': 'text/plain'})
        .response.is_(http_response(status_code=400))
        .build()
    )
    stubs.append(
        imposter_client.new_stub_builder()
        .when(http_request.headers == {'Accept': 'application/xml'})
        .response.is_(http_response(status_code=406))
        .build()
    )
    stubs.append(
        imposter_client.new_stub_builder()
        .when(http_request.method == 'PUT')
        .response.is_(http_response(status_code=405))
        .build()
    )
    stubs.append(
        imposter_client.new_stub_builder()
        .when(http_request.method == 'PUT')
        .response.is_(http_response(status_code=500))
        .build()
    )

    imposter_client.create('sample', 'http', 65000, stubs=stubs)

    response = requests.post('http://localhost:65000/test?First=1&Second=2',
                             headers={'accept': 'text/plain'},
                             data='hello, world!')
    assert response.status_code == 400

    response = requests.post('http://localhost:65000/test?First=1&Second=2',
                             headers={'accept': 'application/xml'},
                             data='hello, world!')
    assert response.status_code == 406

    response = requests.put('http://localhost:65000/test?First=1&Second=2',
                            headers={'accept': 'application/json'},
                            data='hello, world!')
    assert response.status_code == 405


def test_imposter_with_deep_equals_predicate(imposter_client):
    imposter_client.delete(65000)
    stubs = []
    stubs.append(
        imposter_client.new_stub_builder()
        .when(http_request.query.deep_equals({}))
        .response.is_(http_response(status_code=200, body='first'))
        .build()
    )

    stubs.append(
        imposter_client.new_stub_builder()
        .when(http_request.query.deep_equals({'first': '1'}))
        .response.is_(http_response(status_code=200, body='second'))
        .build()
    )

    stubs.append(
        imposter_client.new_stub_builder()
        .when(http_request.query.deep_equals({'first': '1', 'second': '2'}))
        .response.is_(http_response(status_code=200, body='third'))
        .build()
    )

    imposter_client.create('sample', 'http', 65000, stubs=stubs)

    response = requests.get('http://localhost:65000/test')
    assert response.text == 'first'

    response = requests.get('http://localhost:65000/test?First=1')
    assert response.text == 'second'

    response = requests.get('http://localhost:65000/test?Second=2&First=1')
    assert response.text == 'third'

    response = requests.get('http://localhost:65000/test?Second=2&First=1&Third=3')
    assert response.text == ''


def test_imposter_with_contains_predicate(imposter_client, socket_factory):
    imposter_client.delete(65000)
    stubs = []
    stubs.append(
        imposter_client.new_stub_builder()
        .when(tcp_request.data.contains('AgM='))
        .response.is_(tcp_response('Zmlyc3QgcmVzcG9uc2U='))
        .build()
    )

    stubs.append(
        imposter_client.new_stub_builder()
        .when(tcp_request.data.contains('Bwg='))
        .response.is_(tcp_response('c2Vjb25kIHJlc3BvbnNl'))
        .build()
    )

    stubs.append(
        imposter_client.new_stub_builder()
        .when(tcp_request.data.contains('Bwg='))
        .response.is_(tcp_response('dGhpcmQgcmVzcG9uc2U='))
        .build()
    )

    imposter_client.create('sample', 'tcp', 65000, stubs=stubs)

    socket = socket_factory('localhost', 65000)
    assert 'Zmlyc3QgcmVzcG9uc2U=' == socket.send_and_recv('__AgM=__')
    assert 'c2Vjb25kIHJlc3BvbnNl' == socket.send_and_recv('__Bwg=__')


def test_imposter_with_starts_with_predicate(imposter_client, socket_factory):
    imposter_client.delete(65000)

    stubs = []
    stubs.append(
        imposter_client.new_stub_builder()
        .when(tcp_request.data.startswith('first'))
        .response.is_(tcp_response('first response'))
        .build()
    )
    stubs.append(
        imposter_client.new_stub_builder()
        .when(tcp_request.data.startswith('second'))
        .response.is_(tcp_response('second response'))
        .build()
    )
    stubs.append(
        imposter_client.new_stub_builder()
        .when(tcp_request.data.startswith('second'))
        .response.is_(tcp_response('third response'))
        .build()
    )

    imposter_client.create('sample', 'tcp', 65000, stubs=stubs)

    socket = socket_factory('localhost', 65000)
    assert 'first response' == socket.send_and_recv('FIRST REQUEST')
    assert 'second response' == socket.send_and_recv('Second Request')


def test_imposter_with_ends_with_predicate(imposter_client, socket_factory):
    imposter_client.delete(65000)

    stubs = []
    stubs.append(
        imposter_client.new_stub_builder()
        .when(tcp_request.data.endswith('AwQ='))
        .response.is_(tcp_response('first response'))
        .build()
    )
    stubs.append(
        imposter_client.new_stub_builder()
        .when(tcp_request.data.endswith('BQY='))
        .response.is_(tcp_response('second response'))
        .build()
    )
    stubs.append(
        imposter_client.new_stub_builder()
        .when(tcp_request.data.endswith('BQY='))
        .response.is_(tcp_response('third response'))
        .build()
    )

    imposter_client.create('sample', 'tcp', 65000, stubs=stubs)

    socket = socket_factory('localhost', 65000)
    assert 'first response' == socket.send_and_recv('AQIDBA==AwQ=')
    assert 'second response' == socket.send_and_recv('AQIDBAUGBQY=')


def assert_stubbed_service(imposter_client, port, expectations):
    imposter = imposter_client.get_by_port(port)
    for key, value in six.iteritems(expectations):
        assert imposter[key] == value
