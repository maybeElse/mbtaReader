from multiprocessing.resource_sharer import stop
from pickletools import read_unicodestring1
from sched import scheduler
import requests
from datetime import date
from typing import Union
from functools import wraps
import mbtaObjects

class MBTAReader(object):
    def __init__(self, key: str=None, raw_json: bool=True):
        self.headers = {'accept': 'application/vnd.api+json'}

        self.key = key
        if key:
            self.headers['X-API-Key'] = self.api
        else:
            print('We\'ll try running without a key! This means that the API will limit us to 20 requests per minute.')

        self.json = raw_json
        if self.json:
            print('Return type set to raw json, straight from the MBTA API!')
        else:
            print('Return type set to simplified objects (all the same data, just easier to get at)!')

    @staticmethod
    def __build_payload(endpoint: str, **kwargs):
        if not endpoint:
            raise NameError('Construction of payload failed: no endpoint specified.')

        payload = {}

        # this is a pretty ugly solution to wrapping stuff up for the api, sorry!
        # the fact that arguments switch between filters/fields and filters/names depending on api endpoint is vexing
        for key,value in kwargs.items():
            if not value: # skip unset arguments
                continue
                
            if type(value) == list:
                value = ",".join(value)
            if type(value) == int:
                value = str(value)

            # because I decided to hide whether the names of arguments are passed to the API as filters, fields, or directly (because I think that's an extra level of complexity which isn't actually needed when using the functions), there's an extra step of sorting them into the correct forms while building the payload
            # ie: 'page[value]', 'fields[value]', or 'filter[value]'

            if key in ('sort','include'):
                payload[key] = value
            elif key in ('offset','limit'):
                payload['page[%s]' % key] = value

            elif key in ('alert','line','prediction','schechedule','shape','vehicle'):
                payload['fields[%s]' % key] = value

            elif key == 'id' and '_by_id' in endpoint:
                payload[key] = value

            elif endpoint in ('routes', 'route_by_id', 'stops', 'stops_by_id',
                    'trips', 'trip_by_id', 'services', 'service_by_id', 'facilities', 'facility_by_id') \
                     and key in ('route', 'stop', 'trip', 'service', 'facility'):
                payload['fields[%s]' % key] = value

            else: # anything not caught in the conditions above should be filters (unless something is badly broken)
                payload['filter[%s]' % key] = value
        return payload

    def __get(self, endpoint: str, payload: dict):
        response = requests.get('https://api-v3.mbta.com/%s' % endpoint.removesuffix('_by_id'), params=payload, headers=self.headers)

        response_json = response.json()
        if not response_json:
            raise ValueError('No data returned from API, check your arguments.')

        if self.json:
            return response_json

    def __ask_the_api(f):
        @wraps(f)
        def wrapper(self, *args, **kwargs):
            endpoint = f(self, *args, **kwargs)
            return self.__get(endpoint, self.__build_payload(endpoint, **kwargs))
        return wrapper

    @__ask_the_api
    def get_alerts(self,
        offset: str=None, limit: str=None, sort: str=None,
        id: Union[str, list]=None,
        route: Union[str, list]=None,
        stop: Union[str, list]=None,
        trip: Union[str, list]=None,
        facility: Union[str, list]=None,
        alert: Union[str, list]=None,
        route_type: Union[str, list]=None,
        direction_id: str=None,
        banner: str=None,
        datetime: str=None,
        lifecycle: Union[str, list]=None,
        severity: Union[str, list]=None,
        activity: Union[str, list]=None):
        endpoint = "alerts"
        return endpoint

    @__ask_the_api
    def get_alert_by_id(self,
        id: str,
        include: Union[str,list]=None,
        alert: Union[str, list]=None):
        endpoint = "alerts_by_id"
        return endpoint

    @__ask_the_api
    def get_facilities(self,
        offset: str=None, limit: str=None, sort: str=None,
        include: Union[str,list]=None,
        stop: Union[str, list]=None,
        facility: Union[str, list]=None,
        type: Union[str, list]=None,):
        endpoint = "facilities"
        return endpoint

    @__ask_the_api
    def get_facility_by_id(self,
        id: str,
        include: Union[str,list]=None,
        facility: Union[str, list]=None):
        endpoint = "facilities_by_id"
        return endpoint

    @__ask_the_api
    def get_lines(self,
        offset: str=None, limit: str=None, sort: str=None,
        id: Union[str, list]=None,
        line: Union[str, list]=None):
        endpoint = "lines"
        return endpoint

    @__ask_the_api
    def get_line_by_id(self,
        id: str,
        include: Union[str,list]=None,
        line: Union[str, list]=None):
        endpoint = "lines_by_id"
        return endpoint

    @__ask_the_api
    def get_live_facilities(self,
        offset: str=None, limit: str=None, sort: str=None,
        include: Union[str,list]=None,
        id: Union[str, list]=None):
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
        offset: str=None, limit: str=None, sort: str=None,
        include: Union[str,list]=None,
        stop: Union[str, list]=None,
        route: Union[str,list]=None,
        trip: Union[str,list]=None,
        prediction: Union[str,list]=None,
        route_type: str=None,
        direction_id: str=None,
        latitude: str=None,
        longitude: str=None,
        radius: str=None,
        route_pattern: str=None):
        endpoint = "predictions"
        return endpoint

    @__ask_the_api
    def get_routes(self,
        offset: str=None,
        limit: str=None,
        sort: str=None,
        include: Union[str,list]=None,
        id: Union[str,list]=None,
        route: Union[str,list]=None,
        stop: Union[str,list]=None,
        type: Union[str,list]=None,
        direction_id: str=None,
        date: str=None):
        endpoint = "routes"
        return endpoint

    @__ask_the_api
    def get_route_by_id(self,
        id: str,
        include: Union[str,list]=None,
        route: Union[str,list]=None):
        endpoint = "routes_by_id"
        return endpoint

    @__ask_the_api
    def get_route_patterns(self,
        offset: str=None,
        limit: str=None,
        sort: str=None,
        include: Union[str,list]=None,
        id: Union[str,list]=None,
        route: Union[str,list]=None,
        stop: Union[str,list]=None,
        direction_id: str=None):
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
        include: Union[str,list]=None,
        route: Union[str,list]=None,
        stop: Union[str,list]=None,
        trip: Union[str,list]=None,
        schedule: Union[str,list]=None,
        route_type: Union[str,list]=None,
        direction_id: str=None,
        date: str=None,
        min_time: str=None,
        max_time: str=None,
        stop_sequence: str=None,):
        endpoint = "schedules"
        return endpoint

    @__ask_the_api
    def get_services(self,
        offset: str=None,
        limit: str=None,
        sort: str=None,
        id: Union[str,list]=None,
        route: Union[str,list]=None,
        service: Union[str,list]=None):
        endpoint = "services"
        return endpoint

    @__ask_the_api
    def get_service_by_id(self,
        id: str,
        service: Union[str,list]=None,):
        endpoint = "services_by_id"
        return endpoint

    @__ask_the_api
    def get_shapes(self,
        offset: str=None,
        limit: str=None,
        sort: str=None,
        include: Union[str,list]=None,
        route: Union[str,list]=None,
        shape: Union[str,list]=None):
        endpoint = "shapes"
        return endpoint

    @__ask_the_api
    def get_shape_by_id(self,
        id: str,
        include: Union[str,list]=None,
        shape: Union[str,list]=None):
        endpoint = "shapes_by_id"
        return endpoint

    @__ask_the_api
    def get_stops(self,
        offset: str=None,
        limit: str=None,
        sort: str=None,
        include: Union[str,list]=None,
        id: Union[str,list]=None,
        route: Union[str,list]=None,
        stop: Union[str,list]=None,
        service: Union[str,list]=None,
        route_type: Union[str,list]=None,
        direction_id: str=None,
        type: str=None,
        latitude: str=None,
        longitude: str=None,
        radius: str=None,
        date: str=None,
        location_type: Union[str,list]=None):
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
        id: Union[str,list]=None,
        route: Union[str,list]=None,
        trip: Union[str,list]=None,
        direction_id: str=None,
        route_pattern: Union[str,list]=None,
        date: str=None,
        name: Union[str,list]=None):
        endpoint = "trips"
        return endpoint

    @__ask_the_api
    def get_trip_by_id(self,
        id: str,
        include: Union[str,list]=None,
        trip: Union[str,list]=None):
        endpoint = "trips_by_id"
        return endpoint

    @__ask_the_api
    def get_vehicles(self,
        offset: str=None,
        limit: str=None,
        sort: str=None,
        include: Union[str,list]=None,
        id: Union[str,list]=None,
        route: Union[str,list]=None,
        trip: Union[str,list]=None,
        vehicle: str=None,
        route_type: Union[str,list]=None,
        direction_id: str=None,
        label: Union[str,list]=None):
        endpoint = "vehicles"
        return endpoint

    @__ask_the_api
    def get_vehicle_by_id(self,
        id: str,
        include: Union[str,list]=None,
        vehicle: str=None):
        endpoint = "vehicles_by_id"
        return endpoint


if __name__ == '__main__':
    api = MBTAReader()

#    print(api.get_prediction(stop='place-portr', limit='3'))
#    print(api.get_alerts(limit='3'))
#    print(api.get_facilities(limit='3'))
    print(api.get_lines(limit='3'))