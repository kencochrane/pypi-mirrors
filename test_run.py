#!/usr/bin/env python

from jinja2 import Environment, FileSystemLoader
from mirrorlib import mirror_statuses

from utils import (find_number_of_packages)

from config import MIRRORS

def process_results(results):
    """ process the results and gather data """

    new_results = []
    for d in results:
        mirror = d.get('mirror')
        status = d.get('status')
        d['location'] = "n/a"
        if  status != 'Unavailable':
            resp_list = ["1","2","3","4","5","6","7","8","9","10"] # faked out for test
            age_list = ["1","2","3","4","5","6","7","8","9","10"] # faked out for test
            d['num_packages'] = find_number_of_packages(mirror)
            d['resp_list'] = ",".join(resp_list)
            d['age_list'] = ",".join(age_list)
        new_results.append(d)
    return new_results


def url_for(something):
    return something

def run():
    """ run everything """
    results = mirror_statuses(mirrors=MIRRORS)
    if results:
        time_now = results[0].get('time_now', None)
    data = process_results(results)

    env = Environment(loader=FileSystemLoader('templates'))
    # add the dummy url_for so it doesn't throw error.
    env.globals.update(url_for=url_for)
    template = env.get_template('index.html')
    context = {'data': data, 'date_now': time_now}
    print template.render(**context)

if __name__ == '__main__':
    run()
