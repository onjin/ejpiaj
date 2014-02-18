Examples
========

Post body
---------

Example::

    requests:
      001_token_post:
        method: post
        url: https://example.com/webapi/v1/token
        headers: ~
        url_params: 
          lang: pl
        form_params: ~
        body: '{"username":"user", "password":"bestpass"}'

        assertions:
          response:
            - 'status_code in 200'
        variables:
          json:
            token: token


Authenticate by header
----------------------

Example::

    requests:
      001_get_token:
        method: post
        url: http://localhost:8000/api/v10/api-token-auth/
        form_params:
          username: apitest
          password: apitest
        variables:
          json:
            token: token
        assertions:
          response:
            - 'status_code equals 200'
          json:
            - 'token notempty'

      002_get_users:
        method: get
        url: http://localhost:8000/api/v10/users/
        headers:
          Authorization: Token {{token}}
        assertions:
          response:
            - 'status_code equals 200'
