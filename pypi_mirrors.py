#!/usr/bin/env python
import datetime
import socket
import urllib2


# Add non-official mirrors here
MIRRORS = [
     'pypi.crate.io',
]
MIRROR_URL = "http://{0}/last-modified"
MASTER_URL = "http://{0}/daytime"

#TODO: replace with a template system and nice html/css
page = """<html><head><title>PyPI Mirror Status</title></head><body>
<h1>PyPI Mirror Status</h1>
<p>Here is a list of the PyPI mirrors and the last time they were updated</p>

{body}

<hr>
Page last updated at {date_now} <br />
Built with:
<a href='https://github.com/kencochrane/pypi-mirrors'>pypi-mirrors</a>
</body>
</html>
"""


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
        res = urllib2.urlopen(mirror_url)
        return res.read().strip()
    except Exception:
        return None


def parse_date(date_str):
    """ parse the date the get back from the mirror """
    if len(date_str) == 17:
        # Used on official mirrors
        date_fmt = '%Y%m%dT%H:%M:%S'
    else:
        # Canonical ISO-8601 format (compliant with PEP 381)
        date_fmt = '%Y-%m-%dT%H:%M:%S'
    return datetime.datetime.strptime(date_str, date_fmt)


def humanize_date_difference(now, otherdate=None, offset=None):
    """ This function prints the difference between two python datetime objects
    in a more human readable form

    Adapted from:
    http://www.chimeric.de/blog/2008/0711_smart_dates_in_python
    and
    https://gist.github.com/207624
    """
    if otherdate:
        dt = now - otherdate
        delta_d, offset = dt.days, dt.seconds
    elif offset:
        delta_d, offset = divmod(offset, 60 * 60 * 24)
    else:
        raise ValueError("Must supply otherdate or offset (from now)")
    offset, delta_s = divmod(offset, 60)
    delta_h, delta_m = divmod(offset, 60)

    if delta_d:
        fmt = "{d:d} days, {h:d} hours, {m:d} minutes ago"
    elif delta_h:
        fmt = "{h:d} hours, {m:d} minutes ago"
    elif delta_m:
        fmt = "{m:d} minutes, {s:d} seconds ago"
    else:
        fmt = "{s:d} seconds ago"
    return fmt.format(d=delta_d, h=delta_h, m=delta_m, s=delta_s)


def gather_data(now, mirror_url=MIRROR_URL, master_url=MASTER_URL):
    """ get the data we need put in dict """
    # a.pypi.python.org is the master server
    ml = 'a.pypi.python.org'
    m_url = master_url.format(ml)
    res = ping_mirror(m_url)
    ping_results = [(ml, res)]
    for ml in get_mirrors():
        m_url = mirror_url.format(ml)
        res = ping_mirror(m_url)
        ping_results.append((ml, res))

    results = []
    for ml, res in ping_results:
        if res:
            last_update = parse_date(res)
            how_old = humanize_date_difference(now, last_update)
            results.append({'mirror': ml,
                'last_update': last_update,
                'how_old':  how_old}
            )
        else:
            results.append({'mirror': ml,
                'last_update': "Unavailable",
                'how_old':  "Unavailable"}
            )
    return results


def generate_page(format='html'):
    now = datetime.datetime.utcnow()
    data = gather_data(now)
    body = "<table border='1' width='50%'>"
    body += "<tr><th>Mirror</th><th>Last update</th><th>Age</th></tr>"
    row = "<tr><td>{mirror}</td><td>{last_update}</td><td>{how_old}</td></tr>"
    for d in data:
        body += row.format(**d)
    body += "</table>"
    page_out = page.format(body=body, date_now=now)
    print page_out

if __name__ == '__main__':
    generate_page()
