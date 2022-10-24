import json
from datetime import datetime

class MBTAObject(object):
    def __init__(self, api_data: json):
        self.json = api_data

    def __repr__(self):
        return json.dumps(self.json)

    # helper method to convert datetimes returned by the api
    @staticmethod
    def __convert_time__(time: str):
        return datetime.strptime(time, '%Y-%m-%dT%H:%M:%S%z')

class Route(MBTAObject):
    def __init__(self, api_data: json):
        super(self.__class__, self).__init__(api_data)

        if api_data['data']['type'] != 'route':
            raise Exception('json has unexpected type')

        self.route_color = api_data['data']['attributes']['color']
        self.text_color = api_data['data']['attributes']['text_color']
        self.description = api_data['data']['attributes']['description']
        self.fare_class = api_data['data']['attributes']['fare_class']

        self.long_name = api_data['data']['attributes']['long_name']
        self.short_name = api_data['data']['attributes']['short_name']

        self.direction_names = api_data['data']['attributes']['direction_names']
        self.direction_destinations = api_data['data']['attributes']['direction_destinations']

        self.type_name = ('Light Rail','Heavy Rail','Commuter Rail','Bus','Ferry')[api_data['data']['attributes']['type']]

class Prediction(MBTAObject):
    def __init__(self, api_data: json):
        super(self.__class__, self).__init__(api_data)

        if api_data['type'] != 'prediction':
            raise Exception('json has unexpected type')

        self.arrival_time = self.__convert_time__(api_data['attributes']['arrival_time'])
        self.departure_time = self.__convert_time__(api_data['attributes']['departure_time'])
        self.direction_id = api_data['attributes']['direction_id']
        self.schedule_relationship = api_data['attributes']['schedule_relationship']
        self.status =api_data['attributes']['status']
        self.stop_sequence = api_data['attributes']['stop_sequence']


        # relationships
        self.route = api_data['relationships']['route']['data']['id']
        self.stop = api_data['relationships']['stop']['data']['id']
        self.trip = api_data['relationships']['trip']['data']['id']
        self.vehicle = api_data['relationships']['vehicle']['data']['id']


class Predictions(MBTAObject):
    def __init__(self, api_data: json, page_size: int):
        super(self.__class__, self).__init__(api_data)

        self.predictions = []

        for x in api_data['data']:
            self.predictions.append(Prediction(x))

    def __iter__(self):
        return PredictionsIterator(self)

    def __len__(self):
        return len(self.predictions)

class PredictionsIterator:
    def __init__(self, predictions: Predictions):
        self._predictions=predictions
        self._index=0

    def __next__(self):
        if self._index < len(self._predictions):
            result = self._predictions.predictions[self._index]
            self._index += 1
            return result
        raise StopIteration