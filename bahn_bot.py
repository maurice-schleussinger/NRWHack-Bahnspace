# -*- coding: utf-8 -*-
"""
bahn_bot.py

"""
import requests
from datetime import datetime

from pprint import pprint
from rocketchat_API.rocketchat import RocketChat
import config
import time

rocket = RocketChat(
    config.BAHN_BOT_NAME, config.BAHN_BOT_PW, server_url='http://10.82.132.65')


class Event(object):
    """docstring for Event"""

    def __init__(self, e_type, message):
        super(Event, self).__init__()
        self.e_type = e_type

        self.message = message


def announce_event(event):

    rocket.chat_post_message("{0} {1}".format(config.FLAIRS[event.e_type], event.message),
                             channel=config.ANNOUNCE_CHANNEL, alias='RE7').json()


def travel_data(origin_id="556660846", destination_id="000006620", date_info="2017-11-04", time_info="20:00"):
    URL = "http://demo.hafas.de/avv-aachen/restproxy/trip?accessId=avv&originId=L={}&destId=L={}&maxChange=0&date={}&time={}&products=7&format=json&passlist=1".format(
        origin_id, destination_id, date_info, time_info)

    json_data = requests.get(URL).json()

    stops_list = json_data["Trip"][0]["LegList"]["Leg"][0]["Stops"]["Stop"]

    for stop in stops_list[1:]:
        stopdatetime = datetime.strptime(
            " ".join([stop.get("arrDate"), stop.get("arrTime")]), '%Y-%m-%d %H:%M:%S')
        if stopdatetime > datetime.now():
            train_name = json_data["Trip"][0]["LegList"][
                "Leg"][0]["Product"].get("name").strip()
            train_num = json_data["Trip"][0]["LegList"][
                "Leg"][0]["Product"].get("num").strip()
            next_stop = {"stop_name": stop.get('name'), "ext_id": stop.get(
                "extId"), "train_name": train_name, "train_num": train_num}

    return next_stop


def delay(station_id, product_id, train_number, train_name):
    DEPARTURE_URL = "http://demo.hafas.de/avv-aachen/restproxy/departureBoard?id=L={}&accessId=avv&products={}&format=json".format(
        station_id, product_id)
    rt_time = None
    result = requests.get(DEPARTURE_URL)

    departure_data = result.json()
    departures = departure_data['Departure']
    for departure in departures:
        if departure.get('Product').get('num').strip() == train_number and departure.get('Product').get('name').strip() == train_name:
            planned_date = departure.get('date')
            rt_date = departure.get('rtDate')
            planned_time = departure.get('time')
            rt_time = departure.get('rtTime')

    if rt_time:
        rt_data = ' '.join([rt_date, rt_time])
        planned_data = ' '.join([planned_date, planned_time])
        rt_data_dt = datetime.strptime(rt_data, '%Y-%m-%d %H:%M:%S')
        planned_data_dt = datetime.strptime(
            planned_data, '%Y-%m-%d %H:%M:%S')
        delay = rt_data_dt - planned_data_dt
        delay_seconds = delay.seconds
    else:
        delay_seconds = 0

    return delay_seconds

delay_time = 10
c = 1

if __name__ == '__main__':
    while True:

        new_delay = delay(config.STATION_ID, config.PRODUCT_ID,
                          config.TRAIN_NUMBER, config.TRAIN_NAME)
        # new_delay = 840
        if new_delay != delay_time:
            flair = 0
            if new_delay < delay_time:
                flair = 1
            elif new_delay > delay_time:
                flair = -1
            delay_event = Event(
                flair, "Wir haben im Moment {0} min. Verspätung. ⏱️".format(int(new_delay / 60)))
            announce_event(delay_event)
            delay_time = new_delay
        c += 1
        if c % 9 == 0:
            tunnel = Event(
                0, "Wir fahren gleich in einen Tunnel. Nicht erschrecken. 🚇 👻")
            announce_event(tunnel)
        if c % 12 == 0:
            tunnel = Event(
                0, "Nächster Halt {0} 🚉.".format(travel_data()["stop_name"]))
            announce_event(tunnel)
        time.sleep(10)
