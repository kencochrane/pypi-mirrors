pypi-mirrors
============

Very simple tool that pings the PyPI mirrors and tells us when they were updated last. 

I threw this together very quickly as a proof of concept feel free to fork, and send pull requests.

Config
------
It requires redis in order to cache some of the data. For local development it is assuming it to be running
at localhost:6379 db:1 and no password. see ``config.py`` for more info.

In order to get the IP address geolocation lookup to work correctly you need to sign up for an account
from http://ipinfodb.com/register.php and then set an environment variables called ``PYPI_MIRRORS_API_KEY`` with the key they
give you so you can access the API. If you don't have the env variable set, you will not have access to the geo location information.

For installing the API Key on dotCloud you need to run the following command.

   $ dotcloud var set myapp PYPI_MIRRORS_API_KEY=<api key>


How it works
------------
The ``pypi_mirrors.py`` script runs via a cron job and outputs a simple web page. That is all.

Demo
----
http://pypimirrors-kencochrane.dotcloud.com

How to help
-----------
Pick one of the things on the TODO list and implement it and send a pull request.

TODO:
-----
- Create a setup.py and add to PyPI
- Add notifications to mirror maintainers if their mirror is out of sync.
- send out twitter notifications when a mirror is out of date.