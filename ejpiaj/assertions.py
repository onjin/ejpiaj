from .decorators import assertion


@assertion('equals')
def equals_assertion(value, params):
    return str(value) == str(params)


@assertion('notequals')
def notequals_assertion(value, params):
    return not equals_assertion(value, params)


@assertion('in')
def in_assertion(value, params):
    return str(value) in params.split(',')


@assertion('notin')
def notin_assertion(value, params):
    return not in_assertion(value, params)


@assertion('empty')
def empty_assertion(value):
    if value is None:
        return True
    return not str(value)


@assertion('notempty')
def notempty_assertion(value):
    return not empty_assertion(value)
