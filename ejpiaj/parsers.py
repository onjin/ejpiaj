import yaml
import json
import xmltodict


def yaml_parser(filename):
    return yaml.load(open(filename))


def json_parser(filename):
    return json.load(open(filename))


def xml_parser(filename):
    return xmltodict.parse(open(filename))
