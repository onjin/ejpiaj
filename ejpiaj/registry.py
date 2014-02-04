EXTRACTORS = {}
ASSERTIONS = {}


def register_variables_extractor(name, extractor):
    EXTRACTORS[name] = extractor


def unregister_variables_extractor(name):
    del EXTRACTORS[name]


def get_variables_extractors():
    return EXTRACTORS


def get_variables_extractor(name):
    try:
        return EXTRACTORS[name]
    except KeyError:
        raise UnregisteredVariablesExtractor(name)


class UnregisteredVariablesExtractor(Exception):
    pass


def register_assertion(name, assertion):
    ASSERTIONS[name] = assertion


def unregister_assertion(name):
    del ASSERTIONS[name]


def get_assertions():
    return ASSERTIONS


def get_assertion(name):
    try:
        return ASSERTIONS[name]
    except KeyError:
        raise UnregisteredAssertion(name)


class UnregisteredAssertion(Exception):
    pass
