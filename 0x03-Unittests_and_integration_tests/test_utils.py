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
    AsyncMock,
    async_call,
    GithubOrgClient,
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


class TestGetJson(unittest.TestCase):
    """
    TestGetJson class
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        """
        Test that utils.get_json returns the expected result.
        """
        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.json.return_value = test_payload
        self.assertEqual(get_json(test_url), test_payload)
