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
MIRRORS = [
     'pypi.crate.io',
]
MIRROR_URL = "http://{0}/last-modified"
MASTER_URL = "http://{0}/daytime"


def get_mirrors():
    # http://pypi.python.org/mirrors
    res = socket.gethostbyname_ex('last.pypi.python.org')[0]
    last, dot, suffix = res.partition('.')
    assert suffix == 'pypi.python.org'
    mirrors = []
    # the mirrors start with b.pypi.python.org
    for l in range(ord('b'), ord(last) + 1):
        mirrors.append('{0:c}.{1}'.format(l, suffix))
    mirrors.extend(MIRRORS)
    return mirrors


def ping_mirror(mirror_url):
    try:
        start = time.time()
        res = urllib2.urlopen(mirror_url)
        stop = time.time()
        response_time = round((stop - start) * 1000, 2)
        return res.read().strip(), response_time
    except Exception:
        return None, None


def parse_date(date_str):
    """ parse the date the get back from the mirror """
    if len(date_str) == 17:
        # Used on official mirrors
        date_fmt = '%Y%m%dT%H:%M:%S'
    else:
        # Canonical ISO-8601 format (compliant with PEP 381)
        date_fmt = '%Y-%m-%dT%H:%M:%S'
    return datetime.datetime.strptime(date_str, date_fmt)


def humanize_date_difference(now, otherdate=None, offset=None, sign="ago"):
    """ This function prints the difference between two python datetime objects
    in a more human readable form

    Adapted from:
    http://www.chimeric.de/blog/2008/0711_smart_dates_in_python
    and
    https://gist.github.com/207624
    """
    if otherdate:
        dt = abs(now - otherdate)
        delta_d, offset = dt.days, dt.seconds
        if now < otherdate:
            sign = "ahead"
    elif offset:
        delta_d, offset = divmod(offset, 60 * 60 * 24)
    else:
        raise ValueError("Must supply otherdate or offset (from now)")
    offset, delta_s = divmod(offset, 60)
    delta_h, delta_m = divmod(offset, 60)

    if delta_d:
        fmt = "{d:d} days, {h:d} hours, {m:d} minutes {ago}"
    elif delta_h:
        fmt = "{h:d} hours, {m:d} minutes {ago}"
    elif delta_m:
        fmt = "{m:d} minutes, {s:d} seconds {ago}"
    else:
        fmt = "{s:d} seconds {ago}"
    return fmt.format(d=delta_d, h=delta_h, m=delta_m, s=delta_s, ago=sign)


def get_mirror_status(now, last_update):
    """ Get the status of the mirror """
    how_old = abs(now - last_update)

    if how_old < datetime.timedelta(minutes=5):
        return '<span class="label label-success">Excellent</span>'
    elif how_old < datetime.timedelta(minutes=15):
        return '<span class="label label-success">Awesome</span>'
    elif how_old < datetime.timedelta(hours=1):
        return '<span class="label label-success">Great</span>'
    elif how_old < datetime.timedelta(hours=6):
        return '<span class="label label-info">Good</span>'
    elif how_old < datetime.timedelta(hours=12):
        return '<span class="label label-warning">OK</span>'
    elif how_old < datetime.timedelta(days=1):
        return '<span class="label label-warning">Getting stale</span>'
    else:
        return '<span class="label label-important">Out of Date</span>'


def gather_data(mirror_url=MIRROR_URL, master_url=MASTER_URL):
    """ get the data we need put in dict """
    ping_results = []
    for ml in get_mirrors():
        m_url = mirror_url.format(ml)
        res, res_time = ping_mirror(m_url)
        ping_results.append((ml, res, res_time))

    # a.pypi.python.org is the master server
    ml = 'a.pypi.python.org'
    m_url = master_url.format(ml)
    res, res_time = ping_mirror(m_url)
    ping_results.insert(0, (ml, res, res_time))

    now = datetime.datetime.utcnow()
    results = []
    for ml, res, res_time in ping_results:
        if res:
            last_update = parse_date(res)
            how_old = humanize_date_difference(now, last_update)
            status = get_mirror_status(now, last_update)
            results.append({'mirror': ml,
                'last_update': last_update,
                'how_old':  how_old,
                'response_time': res_time,
                'status': status}
            )
        else:
            results.append({'mirror': ml,
                'last_update': "Unavailable",
                'how_old':  "Unavailable",
                'response_time':  "Unavailable",
                'status': '<span class="label">Unavailable</span>'}
            )
    return now, results


def generate_page(format='html'):
    now, data = gather_data()
    body = ""
    row = "<tr><td>{mirror}</td><td>{last_update}</td>" \
          "<td>{how_old}</td><td>{response_time}</td><td>{status}</td></tr>"
    for d in data:
        body += row.format(**d)

    with open(path('template.html'), 'r') as f:
        page = f.read()
    f.close()

    page_out = page.format(body=body, date_now=now)
    print page_out

if __name__ == '__main__':
    generate_page()
