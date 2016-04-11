from .response import ResponseBuilder


class StubBuilder(object):
    def __init__(self):
        self._responses = []
        self._predicates = {}

    @property
    def response(self):
        return ResponseBuilder(self._responses)

    def when(self, *predicates):
        for predicate in predicates:
            # TODO: build in knowledge of and, or, not
            if predicate.operator not in self._predicates:
                self._predicates[predicate.operator] = {}
            merged_predicate = self._predicates[predicate.operator]
            merged_predicate[predicate.field_name] = predicate.value

        return self

    def build(self):
        assert self._responses, 'A stub must have at least one response'
        stub = {
            'responses': self._responses,
        }
        if self._predicates:
            stub['predicates'] = [
                {k: v} for k, v in self._predicates.iteritems()
            ]
        return stub
