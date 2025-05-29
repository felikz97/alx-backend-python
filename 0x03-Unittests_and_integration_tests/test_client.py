#!/usr/bin/env python3
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient  # your class under test

class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")  # <- patch where get_json is used
    def test_org(self, org_name, mock_get_json):
        expected = {"login": org_name, "type": "Organization"}
        mock_get_json.return_value = expected

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main(verbosity=2)

class TestGithubOrgClient(unittest.TestCase):
    def test_public_repos_url(self):
        test_payload = {"repos_url": "https://api.github.com/orgs/testorg/repos"}
        expected_url = "https://api.github.com/orgs/testorg/repos"

        with patch.object(GithubOrgClient, "org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = test_payload
            client = GithubOrgClient("testorg")
            result = client._public_repos_url
            self.assertEqual(result, expected_url)
            mock_org.assert_called_once()


if __name__ == "__main__":
    unittest.main(verbosity=2)