import unittest

from ejpiaj.core import _vars


class TestCore(unittest.TestCase):

    def test_vars_expander(self):
        self.assertEquals(
            _vars('{{var}}', {'var': 1}),
            '1'
        )
        self.assertEquals(
            _vars({'{{key}}': '{{var}}'}, {'var': 1, 'key': 2}),
            {'2': '1'}
        )


if __name__ == '__main__':
    unittest.main()
