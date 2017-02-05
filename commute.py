from configparser import ConfigParser
from datetime import datetime, timedelta

import googlemaps
from pony.orm import commit, db_session

ARRIVAL = datetime(2017, 3, 1, 10, 0)

class GoogleDistance(object):
    def __init__(self):
        config = ConfigParser()
        config.read('settings.ini')
        api_key = config.get('google', 'apikey')
        self.client = googlemaps.Client(key=api_key)

    def commute_work_bicycle(self, prop):
        directions = self.client.directions(
            (prop.position_latitude, prop.position_longitude),
            'One Burlington Plaza, Dublin, Ireland',
            mode='bicycling',
            arrival_time=ARRIVAL)
        # Funky stuff - ensure that we are not across the ocean.
        assert len(directions) == 1
        assert len(directions[0]['legs']) == 1
        prop.distance_bicycle = float(directions[0]['legs'][0]['distance']['value']/1000)
        prop.by_bicycle = timedelta(seconds=directions[0]['legs'][0]['duration']['value'])
        commit()

    def commute_work_transit(self, prop):
        directions = self.client.directions(
            (prop.position_latitude, prop.position_longitude),
            'One Burlington Plaza, Dublin, Ireland',
            mode='transit',
            arrival_time=ARRIVAL)
        assert len(directions) > 0
        assert len(directions[0]['legs']) > 0
        prop.distance_transit = float(directions[0]['legs'][0]['distance']['value']/1000)
        prop.by_transit = timedelta(seconds=directions[0]['legs'][0]['duration']['value'])
        if 'departure_time' in directions[0]['legs'][0]:
            prop.by_transit_start = datetime.fromtimestamp(directions[0]['legs'][0]['departure_time']['value'])
        # Bus = BUS
        # DART = HEAVY_RAIL
        # Luas = TRAM
        for step in directions[0]['legs']:
            if step['travel_mode'] == 'TRANSIT':
                vehicle = step['transit_details']['line']['vehicle']['type']
                if vehicle == 'TRAM':
                    prop.transit_luas = True
                    break
                if vehicle == 'HEAVY_RAIL':
                    prop.transit_dart = True
                    break
