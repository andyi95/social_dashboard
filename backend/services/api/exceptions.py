class BaseAPIException(Exception):
    code = 0
    default_message = 'An error occured during request'

    def __init__(self, code=None, message=None):
        message = self.default_message if not message else message
        code = 0 if not code else code
        self.detail = f'Code: {code} Message: {message}'

    def __str__(self):
        return str(self.detail)


class APIException(BaseAPIException):
    pass

class TokenException(BaseAPIException):
    default_message = 'Invalid access token'


class TooManyRequests(BaseAPIException):
    default_message = 'Too many requests'
