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
    assert expected == stub_builder.build()


def test_build_response_with_predicate(stub_builder):
    stub_builder.when(http_request.body == 'OK') \
        .response.is_(http_response(status_code=200))
    expected = {'predicates': [{'equals': {'body': 'OK'}}],
                'responses': [{'is': {'statusCode': 200}}]}
    assert expected == stub_builder.build()


def test_build_response_with_multiple_predicates(stub_builder):
    stub_builder.when(
        http_request.body == 'OK',
        http_request.path == '/foo'
    ).response.is_(http_response(status_code=200))
    expected = {'predicates': [{'equals': {'body': 'OK',
                                           'path': '/foo'}}],
                'responses': [{'is': {'statusCode': 200}}]}
    assert expected == stub_builder.build()


def test_build_response_with_multiple_different_predicates(stub_builder):
    stub_builder.when(
        http_request.method == 'POST',
        http_request.body.contains('duh')
    ).response.is_(http_response(status_code=200))
    expected = {'predicates': [
        {'contains': {'body': 'duh'}},
        {'equals': {'method': 'POST'}}],
        'responses': [{'is': {'statusCode': 200}}]}
    assert expected['predicates'] == stub_builder.build()['predicates']


def test_build_response_with_not_predicate(stub_builder):
    stub_builder.when(not_(http_request.method == 'POST')) \
        .response.is_(http_response(status_code=200))
    expected = {'predicates': [
        {'not': {'equals': {'method': 'POST'}}}],
        'responses': [{'is': {'statusCode': 200}}]}
    assert expected == stub_builder.build()


def test_build_response_with_and_predicate(stub_builder):
    stub_builder.when(and_(http_request.method == 'POST',
                           http_request.path == '/begin',
                           http_request.body.startswith('duh'))
                      ).response.is_(http_response(status_code=200))
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
    expected = {'predicates': [
        {'or': {'equals': {'method': 'POST'},
                'and': {'equals': {'path': '/begin'},
                        'startsWith': {'body': 'duh'}}

                }
         }
    ],
        'responses': [{'is': {'statusCode': 200}}]}
    assert expected == stub_builder.build()


def test_build_response_with_exists_predicates(stub_builder):
    stub_builder.when(http_request.query.exists('q'),
                      http_request.query.exists('search', False),
                      http_request.headers.exists('Accept'),
                      http_request.headers.exists('X-Rate-Limit', False)
                      ).response.is_(http_response(status_code=200))

    expected = {
        'responses': [{'is': {'statusCode': 200}}],
        'predicates': [
            {
                'exists': {
                    'query': {
                        'q': True,
                        'search': False,
                    },
                    'headers': {
                        'Accept': True,
                        'X-Rate-Limit': False,
                    }
                }
            }
        ]}
    assert expected == stub_builder.build()


def test_build_response_with_equals_predicates(stub_builder):
    stub_builder.when(http_request.method == 'POST',
                      http_request.path == '/test',
                      http_request.query == {'first': '1', 'second': '2'},
                      http_request.headers == {'Accept': 'text/plain'}
                      ).response.is_(http_response(status_code=400))

    expected = {
        'responses': [{'is': {'statusCode': 400}}],
        'predicates': [{
            'equals': {
                'method': 'POST',
                'path': '/test',
                'query': {
                    'first': '1',
                    'second': '2',
                },
                'headers': {
                    'Accept': 'text/plain',
                }
            },
        }]}
    assert expected == stub_builder.build()


def test_build_response_with_deep_equals_predicates(stub_builder):
    stub_builder.when(http_request.query.deep_equals({})
                      ).response.is_(http_response(status_code=200, body='first'))
    expected = {
        'responses': [{'is': {'body': 'first', 'statusCode': 200}}],
        'predicates': [{
            'deepEquals': {
                'query': {}
            }
        }]
    }
    assert expected == stub_builder.build()
