#!/usr/bin/env python

from pypimirrors import mirror_statuses

from utils import (cache_key, location_name, get_total_seconds, 
                   get_connection, store_page_data, find_number_of_packages,
                   get_location_for_mirror)

from config import UNOFFICIAL_MIRRORS

def process_results(results):
    """ process the results and gather data """

    conn = get_connection()
    new_results = []
    for d in results:
        mirror = d.get('mirror')
        resp_time = d.get('response_time')
        age = get_total_seconds(d.get('time_diff'))
        conn.rpush(cache_key('RESPTIME', mirror), resp_time )
        conn.rpush(cache_key('AGE', mirror), age)
        resp_list = conn.lrange(cache_key('RESPTIME', mirror), -60, -1)
        age_list = conn.lrange(cache_key('AGE', mirror), -60, -1)
        location = get_location_for_mirror(mirror)
        d['num_packages'] = find_number_of_packages(mirror)
        d['location'] = location_name(location)
        d['resp_list'] = ",".join(resp_list)
        d['age_list'] = ",".join(age_list)
        new_results.append(d)
    return new_results


def run():
    """ run everything """
    results = mirror_statuses(unofficial_mirrors=UNOFFICIAL_MIRRORS)
    if results:
        time_now = results[0].get('time_now', None)
    data = process_results(results)

    store_page_data(data, time_now)

if __name__ == '__main__':
    run()
