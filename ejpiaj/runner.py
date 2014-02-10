# -*- coding: utf-8 -*-

import logging

import requests
from clint.textui import puts, colored

from .registry import get_variables_extractor, get_assertion


def console_runner(suite, variables=None, debug=False):
    logger = logging.getLogger(__name__)
    failed_counter = 0

    if not variables:
        variables = {}

    puts(colored.white('-' * 80))
    puts(colored.white('P - passed assertions, F - failed assertions'
                       ', V - extracted variables'))
    puts(colored.white('-' * 80))

    tests = suite['requests']
    for test_name in sorted(suite['requests'].keys()):
        test = tests[test_name]
        result = test_request(test, variables)
        logger.debug(result)
        if result['valid']:
            test_name = "%s [P%d,F%d,V%d]" % (
                test_name,
                len(result['passed_assertions']),
                len(result['failed_assertions']),
                len(result['variables']),
            )
            puts(colored.green(
                "✓ " + test_name + " " + str(result['variables'])
            ))
        else:
            failed_counter += 1
            puts(colored.red(
                "✗ " + test_name +
                " (" +
                " ∥ ".join(result['failed_assertions']) + ")"
            ))

    puts(colored.white('-' * 80))

    return failed_counter


def test_request(request, variables):
    method = getattr(requests, request['method'].lower())
    url = _vars(request['url'], variables)
    url_params = None

    failed_assertions = []
    passed_assertions = []
    local_variables = {}
    valid = True

    # headers with applied variables
    headers = _vars(request.get('headers', None), variables)

    # url params with applied variables
    url_params = _vars(request.get('url_params', None), variables)

    # form params with applied variables
    form_params = _vars(request.get('form_params', None), variables)

    # create body data for POST and PUT
    body = None
    if request['method'].lower() in ['post', 'put']:
        if form_params:
            body = form_params
        else:
            body = request.get('body', None)

    response = method(url, params=url_params, data=body, headers=headers)

    # extract variables from response using registered extractors
    if request.get('variables', None):
        for extractor_name, params in request.get('variables').items():
            extractor = get_variables_extractor(extractor_name)
            extractor_variables = extractor(response, params)
            variables.update(extractor_variables)
            local_variables.update(extractor_variables)

    # test assertions using registered extractors
    if request.get('assertions', None):
        for extractor_name, assertions in request.get('assertions').items():
            extractor = get_variables_extractor(extractor_name)
            for assertion in assertions:
                assertion = _vars(assertion, variables)
                if assertion.count(' '):
                    variable, term = assertion.split(' ', 1)
                else:
                    variable = assertion
                value = extractor(response, {variable: 'result'})
                assertion_result = check_assertion(term, value['result'])
                if assertion_result:
                    passed_assertions.append(assertion)
                else:
                    failed_assertions.append(assertion)
                    valid = False

    return {
        'passed_assertions': passed_assertions,
        'failed_assertions': failed_assertions,
        'variables': local_variables,
        'valid': valid,
        'response': response,
        'content': response.content,
    }


def _vars(obj, variables):
    """Set variables in parameters values or body data at .

    Use {{variable_name}} without spaces f.i. in test.yml:

    request_1:
      variables:
        json:
          key: as_name

    request_2:
      url_params
        param: {{as_name}}
    """

    if not obj:
        return

    if isinstance(obj, dict):
        for key, value in obj.items():
            for var_name, var_value in variables.items():
                if var_value is not None:
                    value = value.replace('{{%s}}' % var_name, var_value)
                    obj[key] = value

    if isinstance(obj, str):
        for name, value in variables.items():
            if value is not None:
                obj = obj.replace('{{%s}}' % name, str(value))

    return obj


def check_assertion(expression, value):
    if expression.count(' '):
        assertion_keyword, params = expression.split(' ', 1)
        return get_assertion(assertion_keyword)(value, params)
    else:
        assertion_keyword = expression
        return get_assertion(assertion_keyword)(value)
