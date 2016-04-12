from collections import namedtuple


_Predicate = namedtuple('_Predicate', ['operator', 'field_name', 'value'])


_HighOrderPredicate = namedtuple('HighOrder_Predicate', ['operator', 'operands', 'arity'])


_arity = namedtuple('_arity', ['ONE', 'MULTI'])('ONE', 'MULTI')


class Predicates(object):
    def __init__(self):
        self._predicates = {}

    @classmethod
    def _handle_normal_predicate(cls, merged_predicate, predicate):
        return {predicate.field_name: predicate.value}

    @classmethod
    def _handle_high_order_predicate(cls, merged_predicate, predicate):
        return cls._merge_predicates(predicate.operands)

    @classmethod
    def _merge_predicates(cls, predicates):
        retval = {}
        for predicate in predicates:
            if predicate.operator not in retval:
                retval[predicate.operator] = {}

            merged_predicate = retval[predicate.operator]
            if isinstance(predicate, _Predicate):
                merged_predicate.update(cls._handle_normal_predicate(
                    merged_predicate, predicate))
            elif isinstance(predicate, _HighOrderPredicate):
                merged_predicate.update(cls._handle_high_order_predicate(
                    merged_predicate, predicate))
            else:
                assert False, 'Argument must be of type Predicate or HighOrderPredicate'
        return retval

    def set_predicates(self, *predicates):
        self._predicates = self._merge_predicates(predicates)

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

    def exists(self, value):
        assert type(value) == bool, 'exists() must be called with True/False'
        return _Predicate('exists', self._field_name, value)


def not_(predicate):
    return _HighOrderPredicate('not', [predicate], _arity.ONE)


def and_(*predicates):
    return _HighOrderPredicate('and', predicates, _arity.MULTI)


def or_(*predicates):
    return _HighOrderPredicate('or', predicates, _arity.MULTI)


class HTTPRequest(object):
    request_from = PredicateBuilder('requestFrom')
    path = PredicateBuilder('path')
    query = PredicateBuilder('query')
    method = PredicateBuilder('method')
    headers = PredicateBuilder('headers')
    body = PredicateBuilder('body')
