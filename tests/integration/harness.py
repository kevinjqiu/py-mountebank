import docker


CONTAINER_NAME = 'mountebank-test'

IMPOSTER_HOST = 'localhost'
IMPOSTER_PORT = 2525

docker_client = docker.Client()


def start_imposter(port=IMPOSTER_PORT, stubbed_ports=None):
    print('starting {} on port {}'.format(CONTAINER_NAME, port))
    stubbed_ports = stubbed_ports or []

    port_bindings = {port: port}

    for stubbed_port in stubbed_ports:
        port_bindings[stubbed_port] = stubbed_port

    host_config = docker_client.create_host_config(
        port_bindings=port_bindings)

    response = docker_client.create_container(
        'kevinjqiu/mountebank', ports=[port, 27351, 27352],
        name=CONTAINER_NAME, host_config=host_config)

    if response and response['Id']:
        docker_client.start(container=response['Id'])
        print('{} started on port {}'.format(CONTAINER_NAME, port))


def stop_imposter(port=IMPOSTER_PORT):
    print('stopping {} on port {}'.format(CONTAINER_NAME, port))
    docker_client.stop(CONTAINER_NAME)
    docker_client.remove_container(CONTAINER_NAME)
    print('{} stopped'.format(CONTAINER_NAME, port))
