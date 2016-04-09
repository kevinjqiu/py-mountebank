class ImposterException(StandardError):
    def __init__(self, response):
        self._response = response
