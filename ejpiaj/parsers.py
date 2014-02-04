import yaml


def yaml_parser(yaml_filename):
    return yaml.load(open(yaml_filename))
