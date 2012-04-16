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
                  }
    else:
        # local config
        return { 'host': 'localhost',
                 'port': 6379,
                 'password': None,
                 'db': 0,}
    