import requests
from datetime import datetime

def delay(station_id, product_id, train_number, train_name)
    DEPARTURE_URL = "http://demo.hafas.de/avv-aachen/restproxy/departureBoard?id=L={}&accessId=avv&products={}&format=json".format(station_id, product_id)

    result = requests.get(DEPARTURE_URL)

    departure_data = result.json()
    departures = departure_data['Departure']
    print(len(departures), type(departures))
    for departure in departures:
        print(departure.get('Product'))
        if departure.get('Product').get('num').strip() == train_number and departure.get('Product').get('name').strip() == train_name:
            planned_date = departure.get('date')
            rt_date = departure.get('rtDate')
            planned_time = departure.get('time')
            rt_time = departure.get('rtTime')

    if rt_time:
        rt_data = ' '.join([rt_date, rt_time])
        planned_data = ' '.join([planned_date, planned_time])
        rt_data_dt = datetime.strptime(rt_data, '%Y-%m-%d %H:%M:%S')
        planned_data_dt = datetime.strptime(planned_data, '%Y-%m-%d %H:%M:%S')
        delay = rt_data_dt - planned_data_dt
        delay_seconds = delay.seconds
    else:
        delay_seconds = 0

    return delay_seconds