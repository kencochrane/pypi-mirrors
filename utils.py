import redis
import socket
import requests
import lxml.html

try:
    import cPickle as pickle
except ImportError:
    import pickle

from config import load_config
from iploc import get_city

CONFIG = load_config()

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


def store_page_data(data, time_now):
  """ Store the data in the cache for later use."""
  conn = get_connection()
  context = {'data': data, 'date_now': time_now}
  conn.set('PAGE_DATA', pickle.dumps(context))


def get_page_data():
  """ Get the page data from the cache """
  conn = get_connection()
  data = conn.get('PAGE_DATA')
  if data:
      return pickle.loads(data)
  return None


def get_total_seconds(delta):
    """ need this since timedelta.total_seconds() 
    isn't available in python 2.6.x"""
    if delta:
        return delta.seconds + (delta.days * 24 * 3600)
    return 0


def cache_key(token, value):
    """ build a cache key """
    return "{0}_{1}".format(token, value)


def location_name(location):
    """ build out the location name given the location data """
    if not location:
        return "N/A"
    city = location.get('cityName', None)
    region = location.get('regionName', None)
    country = location.get('countryName', None)
    country_code = location.get('countryCode', None)

    # clear out the -'s
    if city and city == '-':
        city = None
    if region and region == '-':
        region = None

    # If we have everything return everything but only use country_code
    if city and region and country_code:
        return "{0}, {1} {2}".format(city, region, country_code)

    # if we just have country, then only return country
    if not city and not region and country:
        return country

    # whatever else we have build it out by dynamically
    name = ""
    if city:
        name += city
    if city and region:
        name += ", "
    if region:
        name += region + " "
    if country:
        name += country
    return name
