#!/usr/bin/env python3
"""
Unittests for utils.py
"""

import unittest
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized, parameterized_class
from utils import (
    access_nested_map,
    get_json,
    memoize,
)
from fixtures import TEST_PAYLOAD


class TestAccessNestedMap(unittest.TestCase):
    """
    TestAccessNestedMap class
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Test that the method returns what it is supposed to
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected):
        """
        Test that a KeyError is raised for the following inputs
        """
        with self.assertRaises(expected):
            access_nested_map(nested_map, path)
