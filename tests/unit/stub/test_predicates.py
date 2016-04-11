import pytest
from mountebank.stub.predicates import (
    Predicate, HTTPRequest as http_request)


def test_build_predicate_equals():
    expected = Predicate('equals', 'path', '/path')
    assert expected == http_request.path.equals('/path')
    assert expected == (http_request.path == '/path')


def test_build_predicate_deep_equals():
    expected = Predicate('deepEquals', 'path', '/path')
    assert expected == http_request.path.deep_equals('/path')


def test_build_predicate_contains():
    expected = Predicate('contains', 'path', '/path')
    assert expected == http_request.path.contains('/path')


def test_build_predicate_startswith():
    expected = Predicate('startsWith', 'path', '/path')
    assert expected == http_request.path.startswith('/path')


def test_build_predicate_endswith():
    expected = Predicate('endsWith', 'path', '/path')
    assert expected == http_request.path.endswith('/path')


def test_build_predicate_matches():
    expected = Predicate('matches', 'path', '.*path')
    assert expected == http_request.path.matches('.*path')


def test_build_predicate_exists():
    expected = Predicate('exists', 'path', True)
    assert expected == http_request.path.exists(True)


def test_build_predicate_exists_must_be_called_with_boolean():
    with pytest.raises(AssertionError):
        http_request.path.exists('True')
