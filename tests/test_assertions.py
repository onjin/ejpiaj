import unittest

from ejpiaj.runner import check_assertion


class Response(object):
    def __init__(self, content):
        self.content = content


class TestAssertions(unittest.TestCase):

    def test_empty_assertion(self):
        self.assertFalse(check_assertion('empty', 'AA'))
        self.assertFalse(check_assertion('empty', '12'))
        self.assertFalse(check_assertion('empty', '1'))
        self.assertFalse(check_assertion('empty', '0'))
        self.assertFalse(check_assertion('empty', 0))
        self.assertTrue(check_assertion('empty', ''))
        self.assertTrue(check_assertion('empty', None))

    def test_notempty_assertion(self):
        self.assertTrue(check_assertion('notempty', 'AA'))
        self.assertTrue(check_assertion('notempty', '12'))
        self.assertTrue(check_assertion('notempty', '1'))
        self.assertTrue(check_assertion('notempty', '0'))
        self.assertTrue(check_assertion('notempty', 0))
        self.assertFalse(check_assertion('notempty', ''))
        self.assertFalse(check_assertion('notempty', None))

    def test_in_assertion(self):
        self.assertTrue(check_assertion('in 1,2,3,4', 1))
        self.assertTrue(check_assertion('in 1,2,3,4', 2))
        self.assertTrue(check_assertion('in 1,2,3,4', 3))
        self.assertTrue(check_assertion('in 1,2,3,4', 4))
        self.assertTrue(check_assertion('in 1,2,3,4', '4'))
        self.assertFalse(check_assertion('in 1,2,3,4', 6))
        self.assertFalse(check_assertion('in 1,2,3,4', '6'))

    def test_notin_assertion(self):
        self.assertFalse(check_assertion('notin 1,2,3,4', 1))
        self.assertFalse(check_assertion('notin 1,2,3,4', 2))
        self.assertFalse(check_assertion('notin 1,2,3,4', 3))
        self.assertFalse(check_assertion('notin 1,2,3,4', 4))
        self.assertFalse(check_assertion('notin 1,2,3,4', '4'))
        self.assertTrue(check_assertion('notin 1,2,3,4', 6))
        self.assertTrue(check_assertion('notin 1,2,3,4', '6'))
