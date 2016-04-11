import pytest
from mountebank import http_request
from mountebank.stub_builder import StubBuilder, HTTPResponse


@pytest.fixture
def stub_builder():
    return StubBuilder()


def test_build_response_exception_when_no_response(stub_builder):
    with pytest.raises(AssertionError):
        stub_builder.build()


def test_build_response_with_only_status_code(stub_builder):
    stub_builder.response.is_(HTTPResponse(status_code=400))
    expected = {
        'responses': [{
            'is': {
                'statusCode': 400
            }
        }]
    }
    assert expected == stub_builder.build()


def test_build_response_with_multiple_responses(stub_builder):
    stub_builder.response \
        .is_(HTTPResponse(status_code=400)) \
        .is_(HTTPResponse(status_code=200,
                          mode=HTTPResponse.Mode.TEXT,
                          body='OK',
                          headers={'Content-Type': 'text'}))
    expected = {
        'responses': [{
            'is': {
                'statusCode': 400
            }
        }, {
            'is': {
                'statusCode': 200,
                '_mode': 'text',
                'body': 'OK',
                'headers': {'Content-Type': 'text'}
            }
        }]
    }
    stub_builder.build()
    assert expected == stub_builder.build()


def test_build_response_with_predicate(stub_builder):
    stub_builder.when(http_request.body == 'OK') \
        .response.is_(HTTPResponse(status_code=200))
    stub_builder.build()
    expected = {'predicates': [{'equals': {'body': 'OK'}}],
                'responses': [{'is': {'statusCode': 200}}]}
    assert expected == stub_builder.build()


def test_build_response_with_multiple_predicates(stub_builder):
    stub_builder.when(
        http_request.body == 'OK',
        http_request.path == '/foo'
    ).response.is_(HTTPResponse(status_code=200))
    stub_builder.build()
    expected = {'predicates': [{'equals': {'body': 'OK',
                                           'path': '/foo'}}],
                'responses': [{'is': {'statusCode': 200}}]}
    assert expected == stub_builder.build()


def test_build_response_with_multiple_different_predicates(stub_builder):
    stub_builder.when(
        http_request.method == 'POST',
        http_request.body.contains('duh')
    ).response.is_(HTTPResponse(status_code=200))
    stub_builder.build()
    expected = {'predicates': [
        {'contains': {'body': 'duh'}},
        {'equals': {'method': 'POST'}}],
        'responses': [{'is': {'statusCode': 200}}]}
    assert expected == stub_builder.build()
