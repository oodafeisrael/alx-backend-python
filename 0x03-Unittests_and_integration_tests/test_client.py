#!/usr/bin/env python3
"""
Unit tests for the GithubOrgClient class.
"""

import unittest
from unittest import TestCase
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD

#payload = TEST_PAYLOAD[0]


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


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos(self, mock_org):
        """Test _public_repos_url property"""
        mock_org.return_value = {
            'repos_url': 'https://api.github.com/orgs/testorg/repos'
        }
        client = GithubOrgClient('testorg')
        expected_url = 'https://api.github.com/orgs/testorg/repos'
        self.assertEqual(
                client._public_repos_url, expected_url)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license static method"""
        self.assertEqual(
                GithubOrgClient.has_license(
                    repo, license_key), expected)

@parameterized_class([
    {
        "org_payload": TEST_PAYLOAD[0][0],
        "repos_payload": TEST_PAYLOAD[0][1],
        "expected_repos": TEST_PAYLOAD[0][2],
        "apache2_repos": TEST_PAYLOAD[0][3],
    }
])
class TestIntegrationGithubOrgClient(TestCase):
    """Integration test for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Set up mock for requests.get"""
        cls.get_patcher = patch("requests.get")

        # Start patcher and store mock object
        cls.mock_get = cls.get_patcher.start()

        # Side effect to simulate .json() based on URL
        def side_effect(url):
            mock_resp = Mock()
            if url == f"https://api.github.com/orgs/google":
                mock_resp.json.return_value = cls.org_payload
            elif url == cls.org_payload.get("repos_url"):
                mock_resp.json.return_value = cls.repos_payload
            else:
                mock_resp.json.return_value = None
            return mock_resp

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher after all tests"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos method output"""
        client_obj = GithubOrgClient("google")
        self.assertEqual(client_obj.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test filtering repos by license key"""
        client_obj = GithubOrgClient("google")
        self.assertEqual(
            client_obj.public_repos(license="apache-2.0"),
            self.apache2_repos
        )


if __name__ == "__main__":
    unittest.main()
