#!/usr/bin/env python
import datetime
import socket
import urllib2


# Add non-official mirrors here
MIRRORS = [
    # 'pypi.crate.io',
]
MIRROR_URL = "http://{0}/last-modified"

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
    for l in range(ord('a'), ord(last) + 1):
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
        date_fmt = '%Y%m%dT%H:%M:%S'
    else:
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
        offset = dt.seconds + (dt.days * 60 * 60 * 24)
    if offset:
        offset, delta_s = divmod(offset, 60)
        offset, delta_m = divmod(offset, 60)
        offset, delta_h = divmod(offset, 24)
        delta_d = offset
    else:
        raise ValueError("Must supply otherdate or offset (from now)")

    if delta_d > 0:
        return "%d days, %d hours, %d minutes ago" % (delta_d,
                                                     delta_h,
                                                     delta_m)
    if delta_h > 0:
        return "%d hours, %d minutes ago" % (delta_h, delta_m)
    if delta_m > 0:
        return "%d minutes, %d seconds ago" % (delta_m, delta_s)
    else:
        return "%d seconds ago" % delta_s


def gather_data(now, mirror_url=MIRROR_URL):
    """ get the data we need put in dict """
    results = []
    for ml in get_mirrors():
        m_url = mirror_url.format(ml)
        res = ping_mirror(m_url)

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
    row = "<tr><td>{0}</td><td>{1}</td><td>{2}</td></tr>"
    for d in data:
        body += row.format(d.get("mirror", "n/a"),
                        d.get("last_update", "Unavailable"),
                        d.get("how_old", "Unavailable"))
    body += "</table>"
    page_out = page.format(body=body, date_now=now)
    print page_out

if __name__ == '__main__':
    generate_page()
