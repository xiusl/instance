# coding=utf-8
# author:xsl

from flask import make_response
import json


def output_json(data, code, error=None, extra=None):
    msg = data.get('message')
    if msg:
        error = msg
        data = None

    resp_data = {
        'data': data,
        'success': error is None,
        'error': error,
        'extra': extra
    }
    
    resp = make_response(json.dumps(resp_data), code)
    return resp
