import sys


if sys.version_info.major == 2:
    error_base_class = StandardError
elif sys.version_info.major == 3:
    error_base_class = Exception
else:
    raise RuntimeError('Unsupported Python version: {}'.format(sys.version))


class ImposterException(error_base_class):
    def __init__(self, response):
        self._response = response
