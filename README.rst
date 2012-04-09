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

How to help
-----------
Pick one of the things on the TODO list and implement it and send a pull request.

TODO:
-----
- Track results over time, so we can see averages and stability of each mirror (requires a datastore)
- Once we track history add nice pretty charts
- Change to a micro framework like flask and using jinja2 for the templates (not needed until we add more features)
- seperate the web code from the mirror checking code
- make pypi-mirrors a reusable lib that can be used by other projects
- Create a setup.py and add to PyPI
- Add notifications to mirror maintainers if their mirror is out of sync.
- List the physical location of the mirrors