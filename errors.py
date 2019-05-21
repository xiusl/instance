# coding=utf-8
# author:xsl

from instance.utils import output_json


class ApiBaseError(Exception):
    def to_dict(self):
        d = dict([(k, getattr(self, k)) \
                for k in ['code', 'message'] \
                if getattr(self, k)])
        return d


class ResourceDoesNotExist(ApiBaseError):
    code = 404
    message = 'A resource with that ID no longer exists.'


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
