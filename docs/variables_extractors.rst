Variables extractors
====================

Variables extractors are used to extract variables for assertions or to store them and use in next requests.

Builtin variables extractors
----------------------------

response
^^^^^^^^

A ``response`` variables extractor gives you access to attributes of response objects:
 * http://requests.readthedocs.org/en/latest/user/advanced/#request-and-response-objects

Usage::

    variables:
      response:
        status_code: last_code

    assertions:
      response:
        - 'status_code equals 200'

json
^^^^

An ``json`` extractor treats response content as json. You can access json body using python dictionary syntax.

Usage::

    variables:
      json:
        '[0].sha': sha1
        '[1].sha': sha2
        '[2].sha': sha3

    assertions:
      json:
        - 'items.[0].full_name contains ango'

Custom variables extractors
---------------------------

You can easily create your own extractors by creating python file with code::

    import re

    import json

    from ejpiaj.decorators import variable_extractor


    @variable_extractor('json2')
    def json2_variables_extractor(response, variables):
        """Extracts variables from json response.content.

        Variables path are written using 'dot' access and index access to lists
        f.i.:
            some.path.to.list.[0]
            [1].dict.access.later
        """
        result = {}
        re_list = re.compile('^\[\d+\]$')

        # use 'dot' access to dictionary
        data = json.loads(response.content)
        for path, name in variables.items():
            try:
                subdata = data
                for attr in path.split('.'):
                    # support for list access [0]
                    if re_list.match(attr):
                        ind = int(attr[1:-1])
                        subdata = subdata[ind]
                    else:
                        subdata = subdata.get(attr)
                result[name] = subdata
            except:
                result[name] = None
        return result

From now you can use ``json2`` variables extractor in your tests::

    variables:
      json2:
        myvar: varname

by running ``ejpiaj-cli`` with your module::

    $ ejpiaj-cli test --module myfile mytest.yml
