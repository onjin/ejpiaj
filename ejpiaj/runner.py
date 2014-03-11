# -*- coding: utf-8 -*-

import logging

from clint.textui import puts, colored

from .core import test_request


def console_runner(suite, variables=None, debug=False,
                   display_variables=False, quiet=False):
    logger = logging.getLogger(__name__)
    failed_counter = 0

    if not variables:
        variables = {}

    if not quiet:
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
            test_name = u"%s [P%d,F%d,V%d]" % (
                test_name,
                len(result['passed_assertions']),
                len(result['failed_assertions']),
                len(result['variables']),
            )
            if not quiet:
                line = u"✓ " + test_name
                if display_variables:
                    line += " " + str(result['variables'])
                puts(colored.green(line))
        else:
            failed_counter += 1
            if not quiet:
                puts(colored.red(
                    u"✗ " + test_name +
                    u" (" +
                    u" ∥ ".join(result['failed_assertions']) + ")"
                ))

    if not quiet:
        puts(colored.white('-' * 80))

    return failed_counter
