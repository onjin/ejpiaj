from .registry import register_variables_extractor, register_assertion


def variable_extractor(key):
    def decorator(function):
        register_variables_extractor(key, function)
        return function
    return decorator


def assertion(key):
    def decorator(function):
        register_assertion(key, function)
        return function
    return decorator
