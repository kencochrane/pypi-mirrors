#!/usr/bin/env python
import requests
import datetime

mirrors = ['b.pypi.python.org',
            'c.pypi.python.org',
            'd.pypi.python.org',
            'e.pypi.python.org',
            'f.pypi.python.org',
            'g.pypi.python.org']
            
mirror_url = "http://{0}/last-modified"

page = """<html><head><title>PyPI Mirrors</title></head><body>
{body}

<hr>
Build with: <a href='https://github.com/kencochrane/pypi-mirrors'>pypi-mirrors</a><br />
Last updated at {date_now}
</body>
</html>
"""

def ping_mirror(mirror_url):
    res = requests.get(mirror_url)
    if res.ok:
        return res.content.strip()
    return None

def parse_date(date_str):
    """ parse the date the get back from the mirror """
    return datetime.datetime.strptime(date_str,'%Y%m%dT%H:%M:%S')

def humanize_date_difference(now, otherdate=None, offset=None):
    """ This function prints the difference between two python datetime objects
    in a more human readable form
    
    Adapted from:
    http://www.chimeric.de/blog/2008/0711_smart_dates_in_python
    and
    https://gist.github.com/207624 
    """
    if otherdate:
        dt = otherdate - now
        offset = dt.seconds + (dt.days * 60*60*24)
    if offset:
        delta_s = offset % 60
        offset /= 60
        delta_m = offset % 60
        offset /= 60
        delta_h = offset % 24
        offset /= 24
        delta_d = offset
    else:
        raise ValueError("Must supply otherdate or offset (from now)")
        
    if abs(delta_d) > 0:
        return "%d days, %d hours, %d minutes ago" % (abs(delta_d), delta_h, delta_m)
    if delta_h > 0:
        return "%d hours, %d minutes ago" % (delta_h, delta_m)
    if delta_m > 0:
        return "%d minutes, %d seconds ago" % (delta_m, delta_s)
    else:
        return "%d seconds ago" % delta_s

def gather_data():
    """ get the data we need put in dict """
    now = datetime.datetime.now()
    results = []
    for ml in mirrors:
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
    
def generate_page():
    now = datetime.datetime.now()
    data = gather_data()
    body = "<table border='1'><tr><th>Mirror</th><th>Last update</th><th>Age</th></tr>"
    row = "<tr><td>{0}</td><td>{1}</td><td>{2}</td></tr>"
    for d in data:
        body += row.format(d.get("mirror","n/a"), 
                        d.get("last_update","Unavailable"), 
                        d.get("how_old", "Unavailable"))
    body += "</table>"
    page_out = page.format(body=body, date_now=now)
    print page_out

if __name__ == '__main__':
    generate_page()