import pytest
from docker import errors as docker_errors
from mountebank import MountebankClient, ImposterException
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


def assert_stubbed_service(imposter_client, port, expectations):
    imposter = imposter_client.get_by_port(port)
    for key, value in expectations.iteritems():
        assert imposter[key] == value
