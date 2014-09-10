import unittest

from ejpiaj.core import _vars


class TestCore(unittest.TestCase):

    def test_vars_expander(self):
        self.assertEquals(
            _vars('{{var}}', {'var': 1}),
            '1'
        )

        # check original context not changed
        params = {
            'client_secret': 'my_secret',
            'grant_type': 'client_credentials',
            'client_id': 'my_id'
        }
        variables = {
            'url': 'http://127.0.0.1:5000',
        }
        self.assertEquals(
            _vars(params, variables),
            {
                'client_secret': 'my_secret',
                'grant_type': 'client_credentials',
                'client_id': 'my_id'
            }
        )
        self.assertEquals(params, {
            'client_secret': 'my_secret',
            'grant_type': 'client_credentials',
            'client_id': 'my_id'
        })

        # check vars extraction
        params = {
            'client_secret': 'my_secret',
            'grant_type': 'client_credentials',
            'client_id': '{{my_id}}'
        }
        variables = {
            'url': 'http://127.0.0.1:5000',
            'my_id': 'client_id',
        }
        self.assertEquals(
            _vars(params, variables),
            {
                'client_secret': 'my_secret',
                'grant_type': 'client_credentials',
                'client_id': 'client_id'
            }
        )

if __name__ == '__main__':
    unittest.main()
