import pytest
from docker import errors as docker_errors
from mountebank import Imposter
from tests.integration import harness


def teardown_module(module):
    harness.stop_imposter()


@pytest.fixture(scope='module')
def imposter_client():
    imposter_url = harness.start_imposter(stubbed_ports=[65000])
    assert imposter_url is not None
    return Imposter(imposter_url)


def test_imposter_create(imposter_client):
    imposter_client.create('dummy', 'http', 65000)
    assert_stubbed_service(imposter_client, 65000,
                           expectations={
                               'name': 'dummy',
                               'protocol': 'http',
                               'port': 65000,
                           })


def assert_stubbed_service(imposter_client, port, expectations):
    imposter = imposter_client.get_by_port(port)
    for key, value in expectations.iteritems():
        assert imposter[key] == value
