========
Usage
========

Simple usage with **ejpiaj-cli**.

A ``ejpiaj-cli`` tool has one command ``test``::

    $ ejpiaj-cli test --help

    Usage: ejpiaj-cli test <yaml_file> [<debug>] [<module>]

    Run tests using yaml file

    Required Arguments:

      yaml_file

    Options:

       -d --debug   run with debug mode
       -m --module  your module with custom extractors and assertions

A ``yaml_file`` is file with tests. Debug mode (``-d``) displays logs and returns content from requests.

A ``--module`` option allows you to specify own module with custom ``assertions`` and ``variables extractors``.  F.i.::

    $ ejpiaj-cli test ./myapi.yml --module my_module


I will explain idea using example **example_full.yml** file:
 * https://github.com/onjin/ejpiaj/blob/master/examples/example_full.yml

All requests are written under key *requests*. Every request has unique name. It's name is used to sort request while
runing, so numeric prefix is very convinient.

Every request is build from elements:

 * method - request method like 'get', 'post', 'put', 'options' (under the hood is requests library)
 * url - full url to call
 * url_params - params added to url after '?' sign
 * form_params - params used with POST method and PUT
 * body - POST or PUT body, if used then 'form_params' will be skipped
 * variables - variables to extract using registered variables extractors
 * assertions - assertions to run using also variables extractors and registered assertions

Simple example
--------------

First example::

    requests:
      001_search_repos_with_django_in_name:
        method: get
        url: https://api.github.com/search/repositories
        url_params:
          q: django
          sort: stars
          order: desc

Run it with::

    ejpiaj-cli test examples/example_001.yml

The result should be::

    --------------------------------------------------------------------------------
    P - passed assertions, F - failed assertions, V - extracted variables
    --------------------------------------------------------------------------------
    ✓ 001_search_repos_with_django_in_name [P0,F0,V0] {}
    --------------------------------------------------------------------------------

**P0** means 0 passed assertions, **F0** means 0 failed assertions, **V0** means 0 extracted variables

Assertions
----------

Now we are going to add first assertions::

    requests:
      001_search_repos_with_django_in_name:
        method: get
        url: https://api.github.com/search/repositories
        url_params:
          q: django
          sort: stars
          order: desc
        assertions:
          response:
            - 'status_code equals 200'
          json:
            - 'items.[0].full_name contains ango'

Run it with::

    ejpiaj-cli test examples/example_002.yml

The result should be::

    --------------------------------------------------------------------------------
    P - passed assertions, F - failed assertions, V - extracted variables
    --------------------------------------------------------------------------------
    ✓ 001_search_repos_with_django_in_name [P2,F0,V0] {}
    --------------------------------------------------------------------------------

Under key *assertions* we put any variables extractor registered name (json, request).
Under this key we put list of assertions in format::

    variable assertions parameter

**variables** is variable extractor parameter, **assertion** is assertion keyword and **parameter** is optional
parameter for assertion (depends on assertion type)

In this example we used *response* extractor::

    response:
     - 'status_code equals 200'

So we told *response* extractor to get *status_code* attribute from response object and test if it equals to *200*

We used also *json* extractor::

    json:
      - 'items.[0].full_name contains ango'

So we told *json* extractor to get *items.[0].full_name* from response::

    {
      "total_count": 29532,
      "items": [
        {
          "id": 4164482,
          "name": "Django",
          "full_name": "django/django",
          "owner": {
            ...
          },
        }
    }

and check if the *full_name* contains word *ango*

Variables exctracting
---------------------

We can use variables extractors to extract and store variables for further usage in next requests.

Extracting and using variables::

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

Run it with::

    ejpiaj-cli test examples/example_003.yml

The result should be::

    --------------------------------------------------------------------------------
    P - passed assertions, F - failed assertions, V - extracted variables
    --------------------------------------------------------------------------------
    ✓ 001_search_repos_with_django_in_name [P2,F0,V2] {'count': 29532, 'repo_name': u'django/django'}
    ✓ 002_get_commits_from_first_repo [P1,F0,V0] {}
    --------------------------------------------------------------------------------


We simply added **variables** key and used same variable extractor as in *assertions*::

    variables:
      json:
        total_count: count
        items.[0].full_name: repo_name

And now we have variables::

    count = 29532
    repo_name = django/django

And we can use those variables in next request::

    002_get_commits_from_first_repo:
      method: get
      url: https://api.github.com/repos/{{repo_name}}/commits

Variables are put between '{{' and '}}' and **can't** contains spaces'. For example::

    {{repo_name}} - it's good
    {{ repo_nama}} - it's wrong

Full example
------------

Now you can could understand full example at file:
 * https://github.com/onjin/ejpiaj/blob/master/examples/example_full.yml


