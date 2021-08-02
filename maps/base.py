# coding=utf-8
# author:xsl

def mapping(api, prefix, maps):
    for k, v in maps.items():
        path = prefix + v
        api.add_resource(k, path)
