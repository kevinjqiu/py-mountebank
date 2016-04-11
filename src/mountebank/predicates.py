class Predicate(object):
    """Represents a mountebank stub predicate
    """
    def __init__(self, operator, field_name, value):
        self.operator = operator
        self.field_name = field_name
        self.value = value


class PredicateBuilder(object):
    def __init__(self, field_name):
        self._field_name = field_name

    def __eq__(self, other):
        return self.equals(other)

    def equals(self, other):
        return Predicate('equals', self._field_name, other)

    def deep_equals(self, other):
        return Predicate('deepEquals', self._field_name, other)

    def contains(self, other):
        return Predicate('contains', self._field_name, other)


class HTTPRequest(object):
    request_from = PredicateBuilder('requestFrom')
    path = PredicateBuilder('path')
    query = PredicateBuilder('query')
    method = PredicateBuilder('method')
    headers = PredicateBuilder('headers')
    body = PredicateBuilder('body')
    inject = PredicateBuilder('inject')
