import pytest
from mountebank.stub.predicates import _Predicate, http_request


def test_build_predicate_equals():
    expected = _Predicate('equals', 'path', '/path')
    assert expected == http_request.path.equals('/path')
    assert expected == (http_request.path == '/path')


def test_build_predicate_deep_equals():
    expected = _Predicate('deepEquals', 'path', '/path')
    assert expected == http_request.path.deep_equals('/path')


def test_build_predicate_contains():
    expected = _Predicate('contains', 'path', '/path')
    assert expected == http_request.path.contains('/path')


def test_build_predicate_startswith():
    expected = _Predicate('startsWith', 'path', '/path')
    assert expected == http_request.path.startswith('/path')


def test_build_predicate_endswith():
    expected = _Predicate('endsWith', 'path', '/path')
    assert expected == http_request.path.endswith('/path')


def test_build_predicate_matches():
    expected = _Predicate('matches', 'path', '.*path')
    assert expected == http_request.path.matches('.*path')


def test_build_predicate_exists():
    expected = _Predicate('exists', 'path', True)
    assert expected == http_request.path.exists(True)


def test_build_predicate_exists_must_be_called_with_boolean():
    with pytest.raises(AssertionError):
        http_request.path.exists('True')
