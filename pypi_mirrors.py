#!/usr/bin/env python
import datetime
import socket
import urllib2
import os
import time

ROOT = os.path.abspath(os.path.dirname(__file__))
# Used to absolute-ify relative paths
path = lambda x: os.path.abspath(os.path.join(ROOT, x))

# Add non-official mirrors here
UNOFFICIAL_MIRRORS = [
     'pypi.crate.io',
]

STATUSES = {'Excellent':'<span class="label label-success">Excellent</span>',
            'Awesome':'<span class="label label-success">Awesome</span>',
            'Great':'<span class="label label-success">Great</span>',
            'Good':'<span class="label label-info">Good</span>',
            'OK':'<span class="label label-warning">OK</span>',
            'Getting stale':'<span class="label label-warning">Getting stale</span>',
            'Out of Date': '<span class="label label-important">Out of Date</span>'}

from pypimirrors import mirror_statuses

def find_status(status):
    return STATUSES.get(status, 'Unavailable')

def generate_page(format='html'):
    results = mirror_statuses(unofficial_mirrors=UNOFFICIAL_MIRRORS)
    if results:
        now = results[0].get('time_now', None)
    body = ""
    row = "<tr><td><a target='_new' href='http://{mirror}'>{mirror}</a></td>" \
          "<td>{last_update}</td>" \
          "<td>{time_diff_human}</td><td>{response_time}</td><td>{status}</td></tr>"
    for d in results:
        d['status'] = find_status(d.get('status', None))
        body += row.format(**d)

    with open(path('template.html'), 'r') as f:
        page = f.read()
    f.close()

    page_out = page.format(body=body, date_now=now)
    print page_out

if __name__ == '__main__':
    generate_page()
