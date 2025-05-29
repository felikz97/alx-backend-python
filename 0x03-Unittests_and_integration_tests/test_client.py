#!/usr/bin/env python3
import unittest
import requests
from unittest.mock import patch
from aprameterized import parameterized
from client import GithubOrgClient  # Adjust path as needed


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient."""
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json, client.requests.get")
    def test_org(self, org_name, mock_get_json):
        """Test that org method returns the expected organization data."""
        expected = {"login": org_name, "type": "Organization"}
        mock_get_json.return_value = expected

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, expected)
    @patch("utils.requests.get")
    def test_org(self, org_name, mock_get_json):
        expected = {"login": org_name, "type": "Organization"}
        mock_get_json.return_value = expected

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
