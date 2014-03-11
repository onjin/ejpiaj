===============================
ejpiaj
===============================

.. image:: https://badge.fury.io/py/ejpiaj.png
    :target: http://badge.fury.io/py/ejpiaj
    
.. image:: https://travis-ci.org/onjin/ejpiaj.png?branch=master
        :target: https://travis-ci.org/onjin/ejpiaj

.. image:: https://pypip.in/d/ejpiaj/badge.png
        :target: https://pypi.python.org/pypi/ejpiaj

.. image:: https://pypip.in/license/ejpiaj/badge.png




License
-------

* Free software: BSD license

Features
--------

 * describe your API requests in single file (YAML, JSON and XML at this moment) so you can store you API tests with code
   in same repository (f.i. as ejpiaj.json file)
 * file format is detected from file extension ``.yml``, ``.json`` and ``.xml``
 * extract variables from responses and store them to use in next requests (f.i. to get and use authorization token)
 * write assertions agains responses
 * register your own variables extractors and assertions
 * run suite using ``ejpiaj-cli test -m my_addons -s tests.yml`` command

Sample yml file::

    requests:
      001_search_repos_with_django_in_name:
        method: get
        url: https://api.github.com/search/repositories
        url_params:
          q: django
          sort: stars
          order: desc
        variables:
          json:
            total_count: count
            items.[0].full_name: repo_name
        assertions:
          response:
            - 'status_code equals 200'
          json:
            - 'items.[0].full_name contains ango'

      002_get_commits_from_first_repo:
        method: get
        url: https://api.github.com/repos/{{repo_name}}/commits
        assertions:
          response:
            - 'status_code equals 200'

Run it::

    $ ejpiaj-cli test sample.yml -s

    --------------------------------------------------------------------------------
    P - passed assertions, F - failed assertions, V - extracted variables
    --------------------------------------------------------------------------------
    ✓ 001_search_repos_with_django_in_name [P2,F0,V2] {'count': 29754, 'repo_name': u'django/django'}
    ✓ 002_get_commits_from_first_repo [P1,F0,V0] {}
    --------------------------------------------------------------------------------

SNI note
--------
In order to support `SNI`_ in python 2.6/2.7 you need to install additional packages:

* `pyOpenSSL`, a Python wrapper module around the OpenSSL library.
* `ndg-httpsclient`, enhanced HTTPS support for httplib and urllib2.
* `pyasn1`, ASN.1 types and codecs.

.. _`SNI`: http://en.wikipedia.org/wiki/Server_Name_Indication


Documentation
-------------
* http://ejpiaj.readthedocs.org/en/latest/
