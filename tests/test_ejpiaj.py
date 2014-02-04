#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_ejpiaj
----------------------------------

Tests for `ejpiaj` module.
"""

import unittest

from ejpiaj import registry


def extractor1():
    pass


def extractor2():
    pass


class TestEjpiajVariablesRegistry(unittest.TestCase):

    def test_default_registry(self):
        registry.register_variables_extractor('ex1', extractor1)
        registry.register_variables_extractor('ex2', extractor2)
        self.assertEquals(
            registry.get_variables_extractor('ex1'),
            extractor1
        )
        self.assertEquals(
            registry.get_variables_extractor('ex2'),
            extractor2
        )


if __name__ == '__main__':
    unittest.main()
