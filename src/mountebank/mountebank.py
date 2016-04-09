import requests
from .imposter import Imposter


class MountebankClient(object):
    def __init__(self, mountebank_url):
        self._mountebank_url = mountebank_url

    @property
    def imposter(self):
        return Imposter('{}/imposters'.format(self._mountebank_url))
