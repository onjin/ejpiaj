import unittest
import json

from ejpiaj.variable_extractor import json_variables_extractor


class Response(object):
    def __init__(self, content):
        self.content = content


class TestJsonVariablesxtractor(unittest.TestCase):

    def test_flat_extract(self):
        variables = {
            'var1': 'target1',
            'var2': 'target2',
        }
        response = Response(json.dumps({
            'var1': 'data1',
            'var2': 'data2',
        }))
        result = json_variables_extractor(response, variables)

        self.assertEquals(result['target1'], 'data1')
        self.assertEquals(result['target2'], 'data2')

    def test_children_extract(self):
        variables = {
            'var1.var11': 'target1',
            'var1.var22': 'target2',
        }
        response = Response(json.dumps({
            'var1': {'var11': 'data11', 'var22': 'data22'},
        }))
        result = json_variables_extractor(response, variables)

        self.assertEquals(result['target1'], 'data11')
        self.assertEquals(result['target2'], 'data22')

    def test_list_extract(self):
        variables = {
            '[0].var1.var22.[2]': 'target1',
            '[1].var5.var52': 'target2',
        }
        response = Response(json.dumps([
            {'var1': {'var11': 'data11', 'var22': [1, 2, 3]}, },
            {'var5': {'var51': 'data51', 'var52': 'data52'}, },
        ]))
        result = json_variables_extractor(response, variables)

        self.assertEquals(result['target1'], 3)
        self.assertEquals(result['target2'], 'data52')

    def test_list_with_children_with_list_extract(self):
        variables = {
            'items.[0].item_name': 'target1',
            'items.[1].item_name': 'target2',
        }
        response = Response(json.dumps(
            {
                'items': [
                    {'item_name': 'name1', 'var22': [1, 2, 3]},
                    {'item_name': 'name2', 'var22': [1, 2, 3]},
                ],
                'total_count': 2
            },
        ))
        result = json_variables_extractor(response, variables)

        self.assertEquals(result['target1'], 'name1')
        self.assertEquals(result['target2'], 'name2')
