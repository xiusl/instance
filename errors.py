# coding=utf-8
# author:xsl


class ApiBaseError(Exception):
    def to_dict(self):
        d = dict([(k, getattr(self, k)) \
                for k in ['code', 'message'] \
                if getattr(self, k)])
        return d


class ResourceDoesNotExist(ApiBaseError):
    code = 404
    message = 'A resource with that ID no longer exists.'


class LoginRequiredError(ApiBaseError):
    code = 401
    message = 'Please login'

class TipMessageError(ApiBaseError):
    code = 400
    message = "Tip: "
    def __init__(self, tip):
        self.tip = tip
        self.message = self.message + tip

class OperationForbiddenError(ApiBaseError):
    code = 403
    message = 'Operation forbidden'


class MissingRequiredParameter(ApiBaseError):
    code = 400
    message = "Missing required params:"
    def __init__(self, params):
        self.params = params
        self.message = self.message + ', '.join(params)

class BadRequestError(ApiBaseError):
    code = 400
    message = ""

    def __init__(self, msg):
        self.message = self.message + msg
