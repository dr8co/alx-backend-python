#!/usr/bin/env python3
"""
Unittests for client.py
"""

import unittest
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """
    TestGithubOrgClient class
    """

    @parameterized.expand([
        ("google"),
        ("abc"),
    ])
    @patch('client.get_json')
    def test_org(self, test_org, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value
        """
        mock_get_json.return_value = True
        test_client = GithubOrgClient(test_org)
        self.assertEqual(test_client.org, True)
        mock_get_json.assert_called_once()

    def test_public_repos_url(self):
        """
        Test that the result of _public_repos_url is the expected one based
        on the mocked payload
        """
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "http://some_url.com"}
            test_client = GithubOrgClient("some_org")
            self.assertEqual(test_client._public_repos_url,
                             mock_org.return_value["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        Test that the list of repos is what you expect from the chosen payload
        """
        mock_get_json.return_value = TEST_PAYLOAD
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = "http://some_url.com"
            test_client = GithubOrgClient("some_org")
            self.assertEqual(test_client.public_repos(),
                             ["Salty-Hooman", "holbertonschool-csharp"])
            mock_get_json.assert_called_once()

    @parameterized.expand([
        ({'license': {'key': 'my_license'}}, 'my_license', True),
        ({'license': {'key': 'other_license'}}, 'my_license', False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Test that the result of has_license is the expected one based on the
        mocked payload
        """
        test_client = GithubOrgClient("some_org")
        self.assertEqual(test_client.has_license(repo, license_key), expected)
