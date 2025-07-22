#!/usr/bin/env python3
"""
Unit tests for the GithubOrgClient class.
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test case for the GithubOrgClient.org method."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value and
        get_json is called exactly once with the expected URL.
        """
        expected_result = {"login": org_name, "id": 1}
        mock_get_json.return_value = expected_result

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, expected_result)

class TestGithubOrgClient(unittest.TestCase):
    """Test case for GithubOrgClient"""

    @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test the _public_repos_url property"""
        # Define mock return value
        mock_org.return_value = {'repos_url': 'https://api.github.com/orgs/testorg/repos'}

        # Create an instance of the client
        client = GithubOrgClient('testorg')

        # Assert that _public_repos_url returns the expected value
        self.assertEqual(client._public_repos_url, 'https://api.github.com/orgs/testorg/repos')


if __name__ == "__main__":
    unittest.main()
