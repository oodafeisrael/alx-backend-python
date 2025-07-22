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

        mock_get_json.assert_called_once_with(
                f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, expected_result)


class TestGithubOrgClient(unittest.TestCase):
    """Test case for GithubOrgClient"""

    @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test the _public_repos_url property"""
        """Define mock return value"""
        mock_org.return_value = {
                'repos_url': 'https://api.github.com/orgs/testorg/repos'}

        """Create an instance of the client"""
        client = GithubOrgClient('testorg')

        """
        Assert that _public_repos_url returns the
        expected value
        """
        """Assert that _public_repos_url returns the expected value"""
        expected_url = 'https://api.github.com/orgs/testorg/repos'
        self.assertEqual(
                client._public_repos_url, expected_url)


class TestGithubOrgClient(unittest.TestCase):
    """Test case for the GithubOrgClient"""

    @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos(self, mock_org):
        """Unit test for GithubOrgClient._public_repos_url"""
        """Arrange"""
        mock_org.return_value = {
            'repos_url': 'https://api.github.com/orgs/testorg/repos'
        }

        """Act"""
        client = GithubOrgClient('testorg')
        result = client._public_repos_url

        """Assert"""
        self.assertEqual(
                result, 'https://api.github.com/orgs/testorg/repos')

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license returns the correct result"""
        self.assertEqual(
                GithubOrgClient.has_license(repo, license_key), expected)


if __name__ == "__main__":
    unittest.main()
