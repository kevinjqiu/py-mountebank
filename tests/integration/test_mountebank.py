import pytest
from docker import errors as docker_errors
from mountebank import (
    MountebankClient, ImposterException, http_request, http_response)
from tests.integration import harness


def teardown_module(module):
    harness.stop_mb()


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
    stub_builder = imposter_client.new_stub_builder()
    stub_builder.when(http_request.method == 'POST',
                      http_request.path == '/customers/123') \
        .response.is_(
            http_response(status_code=201,
                          headers={
                              'Location': 'http://localhost:4545/customers/123',
                              'Content-Type': 'application/xml'},
                          body='<customer><email>customer@test.com</email></customer>'
                          ))

    imposter_client.create('sample', 'http', 65000, **stubs)


def assert_stubbed_service(imposter_client, port, expectations):
    imposter = imposter_client.get_by_port(port)
    for key, value in expectations.iteritems():
        assert imposter[key] == value
