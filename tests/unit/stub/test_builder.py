import pytest
from mountebank import http_request, http_response, not_, and_, or_
from mountebank.stub.builder import StubBuilder


@pytest.fixture
def stub_builder():
    return StubBuilder()


def test_build_response_exception_when_no_response(stub_builder):
    with pytest.raises(AssertionError):
        stub_builder.build()


def test_build_response_with_only_status_code(stub_builder):
    stub_builder.response.is_(http_response(status_code=400))
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
        .is_(http_response(status_code=400),
             http_response(status_code=200,
                           mode=http_response.Mode.TEXT,
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
        .response.is_(http_response(status_code=200))
    stub_builder.build()
    expected = {'predicates': [{'equals': {'body': 'OK'}}],
                'responses': [{'is': {'statusCode': 200}}]}
    assert expected == stub_builder.build()


def test_build_response_with_multiple_predicates(stub_builder):
    stub_builder.when(
        http_request.body == 'OK',
        http_request.path == '/foo'
    ).response.is_(http_response(status_code=200))
    stub_builder.build()
    expected = {'predicates': [{'equals': {'body': 'OK',
                                           'path': '/foo'}}],
                'responses': [{'is': {'statusCode': 200}}]}
    assert expected == stub_builder.build()


def test_build_response_with_multiple_different_predicates(stub_builder):
    stub_builder.when(
        http_request.method == 'POST',
        http_request.body.contains('duh')
    ).response.is_(http_response(status_code=200))
    stub_builder.build()
    expected = {'predicates': [
        {'contains': {'body': 'duh'}},
        {'equals': {'method': 'POST'}}],
        'responses': [{'is': {'statusCode': 200}}]}
    assert expected == stub_builder.build()


def test_build_response_with_not_predicate(stub_builder):
    stub_builder.when(not_(http_request.method == 'POST')) \
        .response.is_(http_response(status_code=200))
    stub_builder.build()
    expected = {'predicates': [
        {'not': {'equals': {'method': 'POST'}}}],
        'responses': [{'is': {'statusCode': 200}}]}
    assert expected == stub_builder.build()


def test_build_response_with_and_predicate(stub_builder):
    stub_builder.when(and_(http_request.method == 'POST',
                           http_request.path == '/begin',
                           http_request.body.startswith('duh'))
                      ).response.is_(http_response(status_code=200))
    stub_builder.build()
    expected = {'predicates': [
        {'and': {'equals': {'method': 'POST',
                            'path': '/begin'},
                 'startsWith': {'body': 'duh'}
                 }
         }
    ],
        'responses': [{'is': {'statusCode': 200}}]}
    assert expected == stub_builder.build()


def test_build_response_with_or_predicate(stub_builder):
    stub_builder.when(or_(http_request.method == 'POST',
                           http_request.path == '/begin',
                           http_request.body.startswith('duh'))
                      ).response.is_(http_response(status_code=200))
    stub_builder.build()
    expected = {'predicates': [
        {'or': {'equals': {'method': 'POST',
                            'path': '/begin'},
                 'startsWith': {'body': 'duh'}
                 }
         }
    ],
        'responses': [{'is': {'statusCode': 200}}]}
    assert expected == stub_builder.build()


def test_build_response_with_nested_predicates(stub_builder):
    stub_builder.when(or_(http_request.method == 'POST',
                          and_(
                              http_request.path == '/begin',
                              http_request.body.startswith('duh')))
                      ).response.is_(http_response(status_code=200))
    stub_builder.build()
    expected = {'predicates': [
        {'or': {'equals': {'method': 'POST'},
                'and': {'equals': {'path': '/begin'},
                        'startsWith': {'body': 'duh'}}

                }
         }
    ],
        'responses': [{'is': {'statusCode': 200}}]}
    assert expected == stub_builder.build()
