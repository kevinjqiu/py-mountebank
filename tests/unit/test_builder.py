from mountebank.imposter import StubBuilder, HTTPResponse


def test_build_response():
    builder = StubBuilder()
    builder.response.is_(HTTPResponse(status_code=400))
    expected = {
        'responses': [{
            'is': {
                'statusCode': 400
            }
        }]
    }
    assert expected == builder.build()
