#!/usr/bin/env python
import datetime
import socket
import urllib2
import os
import time
import json
import requests
import lxml.html

try:
    import cPickle as pickle
except ImportError:
    import pickle

import redis
from pypimirrors import mirror_statuses
from jinja2 import Environment, PackageLoader

from config import load_config
from iploc import get_city
from utils import cache_key, location_name, get_total_seconds

env = Environment(loader=PackageLoader('pypi_mirrors', 'templates'))
CONFIG = load_config()
ROOT = os.path.abspath(os.path.dirname(__file__))
# Used to absolute-ify relative paths
path = lambda x: os.path.abspath(os.path.join(ROOT, x))

# Add non-official mirrors here
UNOFFICIAL_MIRRORS = [
     'pypi.crate.io',
]


def get_connection():
    """ Get the connection to Redis"""
    return redis.StrictRedis(host=CONFIG.get('host'),
                          port=int(CONFIG.get('port')),
                          db=CONFIG.get('db'),
                          password=CONFIG.get('password'))


def find_number_of_packages(mirror):
    """ Find the number of packages in a mirror """
    html = lxml.html.fromstring(requests.get("http://{0}/simple/".format(mirror)).content)
    return len(html.xpath("//a"))


def ping_ip2loc(ip):
    """ get the location info for the ip
    you need to register for an API key here. http://ipinfodb.com/register.php
    
    and set it as an envirornment variable called
    PYPI_MIRRORS_API_KEY
    
    """
    api_key = CONFIG.get('ip_api_key')
    if not api_key:
        return None
    return get_city(api_key, ip)


def get_location_for_mirror(mirror):
    """ get the location for the mirror """
    conn = get_connection()
    loc_key = cache_key('IPLOC', mirror)
    value = conn.get(loc_key)
    if value:
        return pickle.loads(value)

    ip = socket.gethostbyname(mirror)
    location = ping_ip2loc(ip)
    if location:
        conn.setex(loc_key, 86400, pickle.dumps(location)) # 1 day cache
        return location
    # if we get here, no good, return None
    return None


def generate_page(results, time_now, format='html'):
    """ generate the page from the resutls """
    template = env.get_template('index.html')

    print template.render(date_now=time_now, data=results)


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


def store_results(data, time_now):
    """ Store the data in the cache for later use."""
    conn = get_connection()
    context = {'data': data, 'time_now': time_now}
    conn.set('PAGE_DATA', pickle.dumps(context))


def run():
    """ run everything """
    results = mirror_statuses(unofficial_mirrors=UNOFFICIAL_MIRRORS)
    if results:
        time_now = results[0].get('time_now', None)
    data = process_results(results)

    store_results(data, time_now)
    generate_page(data, time_now)


if __name__ == '__main__':
    run()
