# coding=utf-8
# author:xsl

from flask import g, current_app
from flask_restful import reqparse, Resource
from instance.utils import login_required
from instance.errors import MissingRequiredParameter
import settings
import requests

parser = reqparse.RequestParser()

_args = ['keywords', 'lat', 'lon', 'page']
for _arg in _args:
    parser.add_argument(_arg)


gdurl = 'https://restapi.amap.com/v3/place/around'
type_arr = [
    "010101", "010102",
    "050101","050301","050302","050303","050501","050502","050601",
    "060411","061205",
    "080100","080600",
    "090100",
    "100101","100102","100103",
    "120100","120201","120301","120302",
    "130101","130102","130103",
    "140100","140200","141201",
"150104","170100",]

class LocationRes(Resource):

    @login_required
    def get(self):
        args = parser.parse_args()
        kw = args.get('keywords') or ''
        page = args.get('page') or 1
        lat = args.get('lat')
        lon = args.get('lon')
        if not lat or not lon:
            raise MissingRequiredParameter(['lat', 'lon'])
        
        types = '|'.join(type_arr)
        params = {
             'key': settings.GAODE_KEY,
             'location': '{},{}'.format(lat, lon),
             'sortrule': 'weight',
             'page': page,
             'types': types,
             'radius': 1000
        }
        data = requests.get(gdurl, params)

        return data.json()
