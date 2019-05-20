# coding=utf-8
# author:xsl

from flask import make_response
import json


def output_json(data, code, error=None, headers=None):
    resp_data = {
        'data': data,
        'error': error,
        'success': error is None,
    }
    resp = make_response(json.dumps(resp_data), code)
    resp.headers.extend(headers)
    return resp
