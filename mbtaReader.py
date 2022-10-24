import requests
from datetime import date
from typing import Union
from functools import wraps
import mbtaObjects

class MBTAReader(object):
    def __init__(self, key: str=None, return_xml: bool=True):
        self.headers = {'accept': 'application/vnd.api+json'}

        self.key = key
        if key:
            self.headers['X-API-Key'] = self.api
        else:
            print('We\'ll try running without a key! This means that the API will limit us to 20 requests per minute.')

        self.xml = return_xml
        if self.xml:
            print('Return type set to raw xml, straight from the MBTA API!')
        else:
            print('Return type set to simplified objects (all the same data, just easier to get at)!')

    @staticmethod
    def __build_payload(endpoint: str, **kwargs):
        if not endpoint:
            raise NameError('Construction of payload failed: no endpoint specified.')

        payload = {}

        # this is a pretty ugly solution to wrapping the variables up for the api
        # I'm not sure of a better one
        for key,value in kwargs.items():
            if type(value) == list:
                value = ",".join(value)
            if type(value) == int:
                value = str(value)

            if key in ('sort','include') and value:
                payload[key] = value
            elif key in ('offset','limit') and value:
                payload['page[%s]' % key] = value
            elif key in ('route_type','direction_id','banner','datetime','lifecycle','severity',
                'activity','type','latitude','longitude','radius','route_pattern','date',
                'min_time','max_time','stop_sequence','location_type','name','label') and value:
                payload['filter[%s]' % key] = value
            elif key in ('alert','line','prediction','schechedule','shape','vehicle') and value:
                payload['fields[%s]' % key] = value
            elif key == 'id' and value:
                if '_by_id' in endpoint: payload[key] = value
                else: payload['filter[%s]' % key] = value
            elif key == 'route' and value:
                if 'route' in endpoint: payload['fields[%s]' % key] = value
                else: payload['filter[%s]' % key] = value
            elif key == 'stop' and value:
                if 'stop' in endpoint: payload['fields[%s]' % key] = value
                else: payload['filter[%s]' % key] = value
            elif key == 'trip' and value:
                if 'trip' in endpoint: payload['fields[%s]' % key] = value
                else: payload['filter[%s]' % key] = value
            elif key == 'service' and value:
                if 'service' in endpoint: payload['fields[%s]' % key] = value
                else: payload['filter[%s]' % key] = value
            elif key == 'facility' and value:
                if 'facilit' in endpoint: payload['fields[%s]' % key] = value
                else: payload['filter[%s]' % key] = value
        return payload

    def __get(self, endpoint: str, payload: dict):
        response = requests.get('https://api-v3.mbta.com/%s' % endpoint.removesuffix('_by_id'), params=payload, headers=self.headers)

        response_json = response.json()
        if not response_json:
            raise ValueError('No data returned from API, check your arguments.')

        return response_json

    def __ask_the_api(f):
        @wraps(f)
        def wrapper(self, *args, **kwargs):
            endpoint = f(self, *args, **kwargs)
            return self.__get(endpoint, self.__build_payload(endpoint, **kwargs))
        return wrapper

    @__ask_the_api
    def alerts(self,
        offset: str=None,
        limit: str=None,
        sort: str=None,
        id: str=None):
        endpoint = "alerts"
        return endpoint

    @__ask_the_api
    def alert_by_id(self,
        id: str,
        include: Union[str,list]=None):
        endpoint = "alerts_by_id"
        return endpoint

    @__ask_the_api
    def get_facilities(self,
        offset: str=None,
        limit: str=None,
        sort: str=None,
        include: Union[str,list]=None):
        endpoint = "facilities"
        return endpoint

    @__ask_the_api
    def get_facility_by_id(self,
        id: str,
        include: Union[str,list]=None):
        endpoint = "facilities_by_id"
        return endpoint

    @__ask_the_api
    def get_lines(self,
        offset: str=None,
        limit: str=None,
        sort: str=None,
        id: str=None):
        endpoint = "lines"
        return endpoint

    @__ask_the_api
    def get_line_by_id(self,
        id: str,
        include: Union[str,list]=None):
        endpoint = "lines_by_id"
        return endpoint

    @__ask_the_api
    def get_live_facilities(self,
        offset: str=None,
        limit: str=None,
        sort: str=None,
        include: Union[str,list]=None,
        id: str=None):
        endpoint = "live_facilities"
        return endpoint

    @__ask_the_api
    def get_live_facility_by_id(self,
        id: str,
        include: Union[str,list]=None):
        endpoint = "live_facilities_by_id"
        return endpoint

    @__ask_the_api
    def get_prediction(self,
        offset: str=None,
        limit: str=None,
        sort: str=None,
        include: Union[str,list]=None,
        stop: Union[str, list]=None
    ):
        endpoint = "predictions"
        return endpoint

    @__ask_the_api
    def get_routes(self,
        offset: str=None,
        limit: str=None,
        sort: str=None,
        include: Union[str,list]=None,
        id: str=None):
        endpoint = "routes"
        return endpoint

    @__ask_the_api
    def get_route_by_id(self,
        id: str,
        include: Union[str,list]=None):
        endpoint = "routes_by_id"
        return endpoint

    @__ask_the_api
    def get_route_patterns(self,
        offset: str=None,
        limit: str=None,
        sort: str=None,
        include: Union[str,list]=None,
        id: str=None):
        endpoint = "route_patterns"
        return endpoint

    @__ask_the_api
    def get_route_pattern_by_id(self,
        id: str,
        include: Union[str,list]=None):
        endpoint = "route_patterns_by_id"
        return endpoint

    @__ask_the_api
    def get_schedule(self,
        offset: str=None,
        limit: str=None,
        sort: str=None,
        include: Union[str,list]=None):
        endpoint = "schedules"
        return endpoint

    @__ask_the_api
    def get_services(self,
        offset: str=None,
        limit: str=None,
        sort: str=None,
        id: str=None):
        endpoint = "services"
        return endpoint

    @__ask_the_api
    def get_service_by_id(self,
        id: str):
        endpoint = "services_by_id"
        return endpoint

    @__ask_the_api
    def get_shapes(self,
        offset: str=None,
        limit: str=None,
        sort: str=None,
        include: Union[str,list]=None):
        endpoint = "shapes"
        return endpoint

    @__ask_the_api
    def get_shape_by_id(self,
        id: str,
        include: Union[str,list]=None):
        endpoint = "shapes_by_id"
        return endpoint

    @__ask_the_api
    def get_stops(self,
        offset: str=None,
        limit: str=None,
        sort: str=None,
        include: Union[str,list]=None,
        id: str=None):
        endpoint = "stops"
        return endpoint

    @__ask_the_api
    def get_stops_by_id(self,
        id: str,
        include: Union[str, list]=None,
        stop: Union[str, list]=None):
        endpoint = "stops_by_id"
        return endpoint

    @__ask_the_api
    def get_trips(self,
        offset: str=None,
        limit: str=None,
        sort: str=None,
        include: Union[str,list]=None,
        id: str=None):
        endpoint = "trips"
        return endpoint

    @__ask_the_api
    def get_trip_by_id(self,
        id: str,
        include: Union[str,list]=None):
        endpoint = "trips_by_id"
        return endpoint

    @__ask_the_api
    def get_vehicles(self,
        offset: str=None,
        limit: str=None,
        sort: str=None,
        include: Union[str,list]=None,
        id: str=None):
        endpoint = "vehicles"
        return endpoint

    @__ask_the_api
    def get_vehicle_by_id(self,
        id: str,
        include: Union[str,list]=None):
        endpoint = "vehicles_by_id"
        return endpoint


if __name__ == '__main__':
    api = MBTAReader()

    print(api.get_prediction(stop='place-portr'))