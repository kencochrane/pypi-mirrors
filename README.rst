pypi-mirrors
============

Very simple tool that pings the PyPI mirrors and tells us when they were updated last. 

I threw this together very quickly as a proof of concept feel free to fork, and send pull requests.

How it works
------------
The ``pypi_mirrors.py`` script runs via a cron job and outputs a simple web page. That is all.

Demo
----
http://pypimirrors-kencochrane.dotcloud.com


TODO:
-----
- Track results over time, so we can see averages and stability of each mirror (requires a datastore)
- Once we track history add nice pretty charts
- Change to a micro framework like flask and using jinja2 for the templates (not needed until we add more features)