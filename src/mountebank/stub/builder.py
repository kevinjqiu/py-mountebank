from .response import ResponseBuilder
from .predicates import Predicates


class StubBuilder(object):
    def __init__(self):
        self._responses = []
        self._predicates = Predicates()

    @property
    def response(self):
        return ResponseBuilder(self._responses, self)

    def when(self, *predicates):
        self._predicates.set_predicates(*predicates)
        return self

    def build(self):
        assert self._responses, 'A stub must have at least one response'
        stub = {
            'responses': self._responses,
        }
        stub.update(self._predicates.json)
        return stub
