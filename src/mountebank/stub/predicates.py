import six

from collections import namedtuple


_arity = namedtuple('_arity', ['ONE', 'MULTI'])('ONE', 'MULTI')


def _recursive_dict_merge(dict_a, dict_b, path=None):
    if path is None:
        path = []

    for key in dict_b:
        if key in dict_a:
            if isinstance(dict_a[key], dict) and isinstance(dict_b[key], dict):
                _recursive_dict_merge(dict_a[key], dict_b[key],
                                      path + [str(key)])
            elif dict_a[key] == dict_b[key]:
                pass
            else:
                # Cannot merge non-dict of the same key
                raise RuntimeError(
                    'Conflict at {}'.format('.'.join(path + [str(key)])))
        else:
            dict_a[key] = dict_b[key]

    return dict_a


def _merge_predicates(predicates):
    retval = {}
    for predicate in predicates:
        if predicate.operator not in retval:
            retval[predicate.operator] = {}

        merged_predicate = retval[predicate.operator]
        merged_predicate = _recursive_dict_merge(merged_predicate, predicate.json())

    return retval


class _Predicate(object):
    def __init__(self, operator, field_name, value):
        self.operator = operator
        self.field_name = field_name
        self.value = value

    def json(self):
        return {self.field_name: self.value}


class _HighOrderPredicate(object):
    def __init__(self, operator, operands, arity):
        self.operator = operator
        self.operands = operands
        self.arity = arity

    def json(self):
        return _merge_predicates(self.operands)


class Predicates(object):
    def __init__(self):
        self._predicates = {}

    def set_predicates(self, *predicates):
        self._predicates = _merge_predicates(predicates)

    @property
    def json(self):
        if not self._predicates:
            return {}

        return {
            'predicates': [
                {k: v} for k, v in six.iteritems(self._predicates)]
        }


class PredicateBuilder(object):
    def __init__(self, field_name):
        self._field_name = field_name

    def __eq__(self, value):
        return self.equals(value)

    def equals(self, value):
        return _Predicate('equals', self._field_name, value)

    def deep_equals(self, value):
        return _Predicate('deepEquals', self._field_name, value)

    def contains(self, value):
        return _Predicate('contains', self._field_name, value)

    def startswith(self, value):
        return _Predicate('startsWith', self._field_name, value)

    def endswith(self, value):
        return _Predicate('endsWith', self._field_name, value)

    def matches(self, value):
        return _Predicate('matches', self._field_name, value)

    def exists(self, subkey, value=True):
        return _Predicate('exists', self._field_name, {subkey: value})


def not_(predicate):
    return _HighOrderPredicate('not', [predicate], _arity.ONE)


def and_(*predicates):
    return _HighOrderPredicate('and', predicates, _arity.MULTI)


def or_(*predicates):
    return _HighOrderPredicate('or', predicates, _arity.MULTI)


class http_request(object):
    request_from = PredicateBuilder('requestFrom')
    path = PredicateBuilder('path')
    query = PredicateBuilder('query')
    method = PredicateBuilder('method')
    headers = PredicateBuilder('headers')
    body = PredicateBuilder('body')

    @classmethod
    def exists(cls, subkey, value=True):
        return _Predicate('exists', subkey, value)


class tcp_request(object):
    request_from = PredicateBuilder('requestFrom')
    data = PredicateBuilder('data')
