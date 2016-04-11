from collections import namedtuple


Predicate = namedtuple('Predicate', ['operator', 'field_name', 'value'])

Not = namedtuple('Not', ['predicate'])

And = namedtuple('And', ['predicates'])

Or = namedtuple('Or', ['predicates'])


class Predicates(object):
    def __init__(self):
        self._predicates = {}

    def add_predicates(self, *predicates):
        for predicate in predicates:
            # TODO: build in knowledge of and, or, not
            if predicate.operator not in self._predicates:
                self._predicates[predicate.operator] = {}
            merged_predicate = self._predicates[predicate.operator]
            merged_predicate[predicate.field_name] = predicate.value

    @property
    def json(self):
        if not self._predicates:
            return {}

        return {
            'predicates': [
                {k: v} for k, v in self._predicates.iteritems()]
        }


class PredicateBuilder(object):
    def __init__(self, field_name):
        self._field_name = field_name

    def __eq__(self, value):
        return self.equals(value)

    def equals(self, value):
        return Predicate('equals', self._field_name, value)

    def deep_equals(self, value):
        return Predicate('deepEquals', self._field_name, value)

    def contains(self, value):
        return Predicate('contains', self._field_name, value)

    def startswith(self, value):
        return Predicate('startsWith', self._field_name, value)

    def endswith(self, value):
        return Predicate('endsWith', self._field_name, value)

    def matches(self, value):
        return Predicate('matches', self._field_name, value)

    def exists(self, value):
        assert type(value) == bool, 'exists() must be called with True/False'
        return Predicate('exists', self._field_name, value)


def not_(predicate):
    return Not(predicate)


def and_(*predicates):
    return And(predicates)


def or_(*predicates):
    return Or(predicates)


class HTTPRequest(object):
    request_from = PredicateBuilder('requestFrom')
    path = PredicateBuilder('path')
    query = PredicateBuilder('query')
    method = PredicateBuilder('method')
    headers = PredicateBuilder('headers')
    body = PredicateBuilder('body')
