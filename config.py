import os
import json

def load_config():
    # if at dotcloud load the dotcloud settings
    dotcloud_config = '/home/dotcloud/environment.json'
    if os.path.exists(dotcloud_config):
        env = json.load(open(dotcloud_config))
        return {'host': env['DOTCLOUD_CACHE_REDIS_HOST'],
                  'port': env['DOTCLOUD_CACHE_REDIS_PORT'],
                  'password': env['DOTCLOUD_CACHE_REDIS_PASSWORD'],
                  'db': 1,
                  'ip_api_key': env.get('PYPI_MIRRORS_API_KEY', None),
                  }
    else:
        # local config
        ip_api_key = os.getenv('PYPI_MIRRORS_API_KEY')
        return { 'host': 'localhost',
                 'port': 6379,
                 'password': None,
                 'db': 0,
                 'ip_api_key':ip_api_key}
    