Installation
============

* Install Open Dylan 2011.1 into /opt/opendylan-2011.1.
* Install virtualenv (``pip install virtualenv`` or
  ``easy_install virtualenv``).
* ``virtualenv try.opendylan.org`` to create a new
  virtualenv.
* Activate this new virtualenv:
  ``source try.opendylan.org/bin/activate``.
* Install the requirements for this app:
  ``pip install tornado`` and
  ``pip install celery-with-redis``.
* Install Redis and run it. I recommend using the
  most recent version of Redis 2.4 as earlier versions
  may not work.
* Grab this code and place the root directory of
  the repository on your ``PYTHONPATH``.
* Run ``celeryd -l info`` in the root directory
  of the repository. Running it there lets it find
  the ``celeryconfig.py``.
* Run the Tornado server: ``python server.py``.
* Visit http://localhost:8888/static/index.html.
* Until the 2012.1 release is out, put a symlink
  from ``~/Open-Dylan/`` to ``_build`` in the
  directory where you run celery from.

Issues
======

* Put ``build-*`` directories from the users into an
  appropriate place.
* Better display of compile time errors. Grab the
  log from the build directory that only has the
  build conditions?
* Use a badge from Twitter Bootstrap to indicate the
  warning / error total on the output tab. (This depends
  on the better display of the compile time errors.)
* Timeouts and other errors in Tornado or Celery aren't
  displayed nicely.
