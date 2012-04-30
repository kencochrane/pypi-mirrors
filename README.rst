pypi-mirrors
============

Very simple tool that pings the PyPI mirrors and tells us when they were updated last. 

I threw this together very quickly as a proof of concept feel free to fork, and send pull requests.

Config
------

Redis
~~~~~
It requires redis in order to cache some of the data. For local development it is assuming it to be running
at localhost:6379 db:1 and no password. see ``config.py`` for more info.

GeoIP
~~~~~
In order to get the IP address geolocation lookup, you need to sign up for an account from http://ipinfodb.com/register.php . If you don't have the env variable set, you will not have access to the geo location information. set IPLOC_API_KEY with the API key they give you.

Email & Twitter
~~~~~~~~~~~~~~~

To get the twitter and email notifications to work correctly you need to create an environment.json file in ``/tmp``  with the variables and values shown below.  replace <value> with the real values.

``/tmp/environment.json``::

    {
    "IPLOC_API_KEY": "<value>",
    "TWITTER_CONSUMER_KEY" : "<value>",
    "TWITTER_CONSUMER_SECRET" : "<value>",
    "TWITTER_ACCESS_KEY" : "<value>",
    "TWITTER_ACCESS_SECRET" : "<value>",
    "EMAIL_HOST" : "<value>",
    "EMAIL_PORT" : "<value>",
    "EMAIL_USER" : "<value>",
    "EMAIL_PASSWORD" : "<value>",
    "EMAIL_FROM" : "<value>",
    "EMAIL_TO" : "<value>",
    "EMAIL_BCC" : "<value>",
    "EMAIL_TO_ADMIN": "<value>"
    }


For installing the API Key on dotCloud you need to run the following command. replace <value> with the real values.

env variables::

   dotcloud var set pypimirrors \
       'IPLOC_API_KEY=<value>' \
       'TWITTER_CONSUMER_KEY=<value>' \
       'TWITTER_CONSUMER_SECRET=<value>' \
       'TWITTER_ACCESS_KEY=<value>' \
       'TWITTER_ACCESS_SECRET=<value>' \
       'EMAIL_HOST=<value>' \
       'EMAIL_PORT=<value>' \
       'EMAIL_USER=<value>' \
       'EMAIL_PASSWORD=<value>' \
       'EMAIL_FROM=<value>' \
       'EMAIL_TO=<value>' \
       'EMAIL_BCC=<value>' \
       'EMAIL_TO_ADMIN=<value>'


How it works
------------
The ``pypi_mirrors.py`` script runs via a cron job and puts data into redis. There is one webpage that pull the data from redis and
displays it. There is a daily cron job that runs and sends out notifications if the mirrors are out of date.

Demo
----
http://www.pypi-mirrors.org

How to help
-----------
Pick one of the things on the TODO list and implement it and send a pull request. 

TODO:
-----
- Create a setup.py and add to PyPI
- Add better documentation