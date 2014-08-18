import os
import json

# mirrors listed here
MIRRORS = [
     ('http', 'pypi.douban.com'),
     ('http', 'pypi.hustunique.com'),
     ('http', 'pypi.gocept.com'),
     ('http', 'pypi.tuna.tsinghua.edu.cn'),
     ('http', 'mirror.picosecond.org/pypi'),
     ('http', 'mirrors.aliyun.com/pypi'),
]

EMAIL_OVERRIDE = None # None or "blah@example.com"

def load_config():
    # if at dotcloud load the dotcloud settings
    dotcloud_config = '/home/dotcloud/environment.json'
    if os.path.exists(dotcloud_config):
        env = json.load(open(dotcloud_config))
        return {'host': env['DOTCLOUD_CACHE_REDIS_HOST'],
                  'port': env['DOTCLOUD_CACHE_REDIS_PORT'],
                  'password': env['DOTCLOUD_CACHE_REDIS_PASSWORD'],
                  'db': 1,
                  'ip_api_key': env.get('IPLOC_API_KEY', None),
                  'twitter_consumer_key' : env.get('TWITTER_CONSUMER_KEY', None),
                  'twitter_consumer_secret' : env.get('TWITTER_CONSUMER_SECRET', None),
                  'twitter_access_key' : env.get('TWITTER_ACCESS_KEY', None),
                  'twitter_access_secret' : env.get('TWITTER_ACCESS_SECRET', None),
                  'email_host' : env.get('EMAIL_HOST', None),
                  'email_port' : env.get('EMAIL_PORT', None),
                  'email_user' : env.get('EMAIL_USER', None),
                  'email_password' : env.get('EMAIL_PASSWORD', None),
                  'email_from' : env.get('EMAIL_FROM', None),
                  'email_to' : env.get('EMAIL_TO', None),
                  'email_bcc' : env.get('EMAIL_BCC', None),
                  'email_to_admin': env.get('EMAIL_TO_ADMIN', None),
                  }
    else:
        # local config
        dotcloud_config = '/tmp/environment.json'
        if os.path.exists(dotcloud_config):
            env = json.load(open(dotcloud_config))
            return { 'host': 'localhost',
                     'port': 6379,
                     'password': None,
                     'db': 0,
                     'ip_api_key': env.get('IPLOC_API_KEY', None),
                     'twitter_consumer_key' : env.get('TWITTER_CONSUMER_KEY', None),
                     'twitter_consumer_secret' : env.get('TWITTER_CONSUMER_SECRET', None),
                     'twitter_access_key' : env.get('TWITTER_ACCESS_KEY', None),
                     'twitter_access_secret' : env.get('TWITTER_ACCESS_SECRET', None),
                     'email_host' : env.get('EMAIL_HOST', None),
                     'email_port' : env.get('EMAIL_PORT', None),
                     'email_user' : env.get('EMAIL_USER', None),
                     'email_password' : env.get('EMAIL_PASSWORD', None),
                     'email_from' : env.get('EMAIL_FROM', None),
                     'email_to' : env.get('EMAIL_TO', None),
                     'email_bcc' : env.get('EMAIL_BCC', None),
                     'email_to_admin': env.get('EMAIL_TO_ADMIN', None),
                     }
        else:
            print("can't find a local envirornment file here '/tmp/environment.json' ")
            return None #TODO throw exception?
