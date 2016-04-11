import pytest
from mountebank.stub.predicates import (
    Predicate, HTTPRequest as http_request)


def test_build_predicate_eq():
    expected = Predicate('equals', 'path', '/path')
    assert expected == http_request.path.equals('/path')
