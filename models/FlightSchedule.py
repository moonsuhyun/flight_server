import requests
import models.Secret
import json


class Flight:
    def __init__(self, airline, dept, arri, flight, time, day):
        self.airline = airline
        self.dept = dept
        self.arri = arri
        self.flight = flight
        self.time = time
        self.day = day

    class Day:
        def __init__(self, mon, tue, wed, thu, fri, sat, sun):
            self.mon = mon
            self.tue = tue
            self.wed = wed
            self.thu = thu
            self.fri = fri
            self.sat = sat
            self.sun = sun


def get_departure_schedule(arri):
    url = 'http://apis.data.go.kr/B551177/PaxFltSched/getPaxFltSchedDepartures'
    params = {'serviceKey': models.Secret.get_secret('service_key'), 'numOfRows': '50', 'pageNo': '1', 'lang': 'E', 'airport': arri, 'type': 'json'}
    response = requests.get(url, params=params)
    json_object = json.loads(response.content)
    result = json_object['response']['body']['items']
    flights = []
    for item in result:
        flight = Flight(
            airline=item['airline'],
            dept='ICN',
            arri=item['airportcode'],
            flight=item['flightid'],
            time=item['st'],
            day=Flight.Day(
                True if item['monday'] == 'Y' else False,
                True if item['tuesday'] == 'Y' else False,
                True if item['wednesday'] == 'Y' else False,
                True if item['thursday'] == 'Y' else False,
                True if item['friday'] == 'Y' else False,
                True if item['saturday'] == 'Y' else False,
                True if item['sunday'] == 'Y' else False,
            )
        )
        flights.append(flight)
    return flights


def get_arrival_schedule(dept):
    url = 'http://apis.data.go.kr/B551177/PaxFltSched/getPaxFltSchedArrivals'
    params = {'serviceKey': models.Secret.get_secret('service_key'), 'numOfRows': '50', 'pageNo': '1', 'lang': 'E', 'airport': dept, 'type': 'json'}
    response = requests.get(url, params=params)
    json_object = json.loads(response.content)
    result = json_object['response']['body']['items']
    flights = []
    for item in result:
        flight = Flight(
            airline=item['airline'],
            dept=item['airport'],
            arri='ICN',
            flight=item['flightid'],
            time=item['st'],
            day=Flight.Day(
                True if item['monday'] == 'Y' else False,
                True if item['tuesday'] == 'Y' else False,
                True if item['wednesday'] == 'Y' else False,
                True if item['thursday'] == 'Y' else False,
                True if item['friday'] == 'Y' else False,
                True if item['saturday'] == 'Y' else False,
                True if item['sunday'] == 'Y' else False,
            )
        )
        flights.append(flight)
    return flights

