import requests
from datetime import datetime

def travel_data(origin_id="556660846", destination_id="000006620", date_info="2017-11-04", time_info="20:00"):
    URL = "http://demo.hafas.de/avv-aachen/restproxy/trip?accessId=avv&originId=L={}&destId=L={}&maxChange=0&date={}&time={}&products=7&format=json&passlist=1".format(origin_id, destination_id, date_info, time_info)

    json_data = requests.get(URL).json()

    stops_list = json_data["Trip"][0]["LegList"]["Leg"][0]["Stops"]["Stop"]

    for stop in stops_list[1:]:
        stopdatetime = datetime.strptime(" ".join([stop.get("arrDate"), stop.get("arrTime")]), '%Y-%m-%d %H:%M:%S')
        if stopdatetime > datetime.now():
            train_name = json_data["Trip"][0]["LegList"]["Leg"][0]["Product"].get("name").strip()
            train_num = json_data["Trip"][0]["LegList"]["Leg"][0]["Product"].get("num").strip()
            next_stop = {"stop_name":stop.get('name'), "ext_id":stop.get("extId"), "train_name":train_name, "train_num":train_num}

    return next_stop