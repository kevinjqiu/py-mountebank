import requests
import docker
import retrying


MOUNTEBANK_IMAGE_NAME = 'kevinjqiu/mountebank'
CONTAINER_NAME = 'mountebank-test'

MB_HOST = 'localhost'
MB_PORT = 2525

docker_client = docker.Client()


@retrying.retry(stop_max_attempt_number=5, wait_fixed=500)
def wait_for_service_ready(url):
    response = requests.get(url)
    response.raise_for_status()
    return True


def start_mb(port=MB_PORT, stubbed_ports=None):
    print('starting {} on port {}'.format(CONTAINER_NAME, port))
    stubbed_ports = stubbed_ports or []

    port_bindings = {port: port}

    for stubbed_port in stubbed_ports:
        port_bindings[stubbed_port] = stubbed_port

    host_config = docker_client.create_host_config(
        port_bindings=port_bindings)

    docker_client.pull(MOUNTEBANK_IMAGE_NAME)
    response = docker_client.create_container(
        MOUNTEBANK_IMAGE_NAME, ports=[port, 27351, 27352],
        name=CONTAINER_NAME, host_config=host_config)

    if response and response['Id']:
        docker_client.start(container=response['Id'])
        mb_url = 'http://{}:{}'.format(MB_HOST, port)
        wait_for_service_ready(mb_url)
        print('{} started on port {}'.format(CONTAINER_NAME, port))
        return mb_url

    return None


def stop_mb(port=MB_PORT):
    print('stopping {} on port {}'.format(CONTAINER_NAME, port))
    docker_client.stop(CONTAINER_NAME)
    docker_client.remove_container(CONTAINER_NAME)
    print('{} stopped'.format(CONTAINER_NAME, port))
