import json, urllib, urllib2


def get_city(apikey, ip):
    """ get city location for an ip """
    base_url = "http://api.ipinfodb.com/v3/ip-city/"
    variables = {"format":"json",
                "key":apikey,
                "ip":ip,}

    urldata = urllib.urlencode(variables)
    url = "{0}?{1}".format(base_url, urldata)
    urlobj = urllib2.urlopen(url)
    data = urlobj.read()
    urlobj.close()
    return json.loads(data)
    