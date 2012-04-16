

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
