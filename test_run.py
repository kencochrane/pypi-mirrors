#!/usr/bin/env python

from jinja2 import Environment, FileSystemLoader
from pypimirrors import mirror_statuses

from utils import (location_name, get_total_seconds, find_number_of_packages)

from config import UNOFFICIAL_MIRRORS, IGNORE_MIRRORS

def process_results(results):
    """ process the results and gather data """

    new_results = []
    for d in results:
        mirror = d.get('mirror')
        if mirror in IGNORE_MIRRORS:
            # skip mirrors we want to ignore.
            continue
        status = d.get('status')
        d['location'] = "n/a"
        if  status != 'Unavailable':
            resp_time = d.get('response_time')
            age = get_total_seconds(d.get('time_diff'))
            resp_list = ["1","2","3","4","5","6","7","8","9","10"] # faked out for test
            age_list = ["1","2","3","4","5","6","7","8","9","10"] # faked out for test
            d['num_packages'] = find_number_of_packages(mirror)
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

    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('index.html')
    context = {'data': data, 'date_now': time_now}
    print template.render(**context)

if __name__ == '__main__':
    run()
