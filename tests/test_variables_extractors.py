import unittest
import json

from ejpiaj.variable_extractor import (
    json_variables_extractor,
    response_variables_extractor
)


class Response(object):
    def __init__(self, content=None):
        self.content = content


class TestJsonVariablesExtractor(unittest.TestCase):

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

        self.assertEqual(result['target1'], 'data1')
        self.assertEqual(result['target2'], 'data2')

    def test_children_extract(self):
        variables = {
            'var1.var11': 'target1',
            'var1.var22': 'target2',
        }
        response = Response(json.dumps({
            'var1': {'var11': 'data11', 'var22': 'data22'},
        }))
        result = json_variables_extractor(response, variables)

        self.assertEqual(result['target1'], 'data11')
        self.assertEqual(result['target2'], 'data22')

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

        self.assertEqual(result['target1'], 3)
        self.assertEqual(result['target2'], 'data52')

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

        self.assertEqual(result['target1'], 'name1')
        self.assertEqual(result['target2'], 'name2')

    def test_notexisting_path(self):
        variables = {
            'items.[0].item_name': 'target1',
            'items.[1].item_name': 'target2',
        }
        response = Response(json.dumps(
            {
                'items': [
                    {'item_name': 'name1', 'var22': [1, 2, 3]},
                ],
                'total_count': 1
            },
        ))
        result = json_variables_extractor(response, variables)

        self.assertEqual(result['target1'], 'name1')
        self.assertEqual(result['target2'], None)


class TestResponseVariablesExtractor(unittest.TestCase):
    def test_attribute_access(self):
        variables = {
            'attribute': 'target1',
            'list.[0]': 'target2',
            'list.[1].value': 'target3',
        }
        response = Response()
        response.attribute = 'val1'
        response.list = ['val2', {'value': 'val3'}]

        result = response_variables_extractor(response, variables)

        self.assertEqual(result['target1'], 'val1')
        self.assertEqual(result['target2'], 'val2')
        self.assertEqual(result['target3'], 'val3')

if __name__ == '__main__':
    unittest.main()
