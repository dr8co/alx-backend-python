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
        Test that utils.get_json returns the expected result
        """
        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.json.return_value = test_payload

        actual_result = get_json(test_url)
        self.assertEqual(actual_result, test_payload)
        mock_get.assert_called_once()


class TestMemoize(unittest.TestCase):
    """
    TestMemoize class
    """

    def test_memoize(self):
        """
        Test that when calling a_property twice, the correct result is
        returned but a_method is only called once using assert_called_once
        """
        class TestClass:
            """
            TestClass
            """

            def a_method(self):
                """
                a_method
                """
                return 42

            @memoize
            def a_property(self):
                """
                a_property
                """
                return self.a_method()

        with patch.object(TestClass, 'a_method') as mock_method:
            test_class = TestClass()
            mock_method.return_value = 42
            value = test_class.a_property
            value = test_class.a_property

            self.assertEqual(value, 42)
            mock_method.assert_called_once()


class TestGithubOrgClient(unittest.TestCase):
    """
    TestGithubOrgClient class
    """

    @parameterized.expand([
        ("google"),
        ("abc"),
    ])
    @patch('client.get_json')
    def test_org(self, test_org, mock_get):
        """
        Test that GithubOrgClient.org returns the correct value
        """
        test_class = GithubOrgClient(test_org)
        test_payload = {"payload": True}

        mock_get.return_value = test_payload

        self.assertEqual(test_class.org, test_payload)
        mock_get.assert_called_once()

    def test_public_repos_url(self):
        """
        Test that the result of _public_repos_url is the expected one based
        on the mocked payload
        """
        with patch.object(GithubOrgClient, 'org',
                          new_callable=PropertyMock) as mock_org:
            test_payload = {"repos_url": "World"}
            mock_org.return_value = test_payload
            test_class = GithubOrgClient(test_payload)

            self.assertEqual(test_class._public_repos_url,
                             test_payload.get("repos_url"))

    @patch('client.get_json')
    def test_public_repos(self, mock_get):
        """
        Test that the list of repos is what you expect from the chosen payload
        """
        with patch.object(GithubOrgClient, '_public_repos_url',
                          new_callable=PropertyMock) as mock_public_repos_url:
            test_payload = [{"name": "Google"}, {"name": "Twitter"}]
            mock_public_repos_url.return_value = "http://testurl"
            mock_get.return_value = test_payload
            test_class = GithubOrgClient(test_payload)

            self.assertEqual(test_class.public_repos(), ["Google", "Twitter"])
            mock_get.assert_called_once()
