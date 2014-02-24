#!/usr/bin/env python
import json
from mirrorlib import mirror_statuses

from utils import (cache_key, location_name, get_total_seconds, 
                   get_connection, store_page_data, find_number_of_packages,
                   get_location_for_mirror, store_json_data)

from config import MIRRORS

def process_results(results):
    """ process the results and gather data """

    conn = get_connection()
    new_results = []
    for d in results:
        mirror = d.get('mirror')
        status = d.get('status')
        location = get_location_for_mirror(mirror)
        d['location'] = location_name(location)
        if  status != 'Unavailable':
            resp_time = d.get('response_time')
            age = get_total_seconds(d.get('time_diff'))
            conn.rpush(cache_key('RESPTIME', mirror), resp_time )
            conn.rpush(cache_key('AGE', mirror), age)
            resp_list = conn.lrange(cache_key('RESPTIME', mirror), -60, -1)
            age_list = conn.lrange(cache_key('AGE', mirror), -60, -1)
            d['num_packages'] = find_number_of_packages(mirror)
            d['resp_list'] = ",".join(resp_list)
            d['age_list'] = ",".join(age_list)
        new_results.append(d)
    return new_results

def json_results(data):
    results = {}
    for mirror in data:
        results[mirror.get('mirror')] = {
            'status': mirror.get('status', 'n/a'),
            'location': mirror.get('location', 'n/a'),
            'num_packages': mirror.get('num_packages', 'n/a'),
            'last_updated': mirror.get('time_diff_human', 'n/a'),
        }
    return json.dumps(results)

def run():
    """ run everything """
    results = mirror_statuses(mirrors=MIRRORS)
    if results:
        time_now = results[0].get('time_now', None)
    data = process_results(results)
    json_data = json_results(data)

    store_json_data(json_data)
    store_page_data(data, time_now)

if __name__ == '__main__':
    run()
