import re

import json

from .decorators import variable_extractor


@variable_extractor('json')
def json_variables_extractor(response, variables):
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


@variable_extractor('response')
def response_variable_extractor(response, variables):
    result = {}
    re_list = re.compile('^\[\d+\]$')
    for path, name in variables.items():
        try:
            subdata = response
            for attr in path.split('.'):
                # support for list access [0]
                if re_list.match(attr):
                    ind = int(attr[1:-1])
                    subdata = subdata[ind]
                else:
                    subdata = getattr(subdata, attr)
            result[name] = subdata
        except:
            result[name] = None
    return result
