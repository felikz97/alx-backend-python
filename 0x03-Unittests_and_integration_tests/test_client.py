#!/usr/bin/env python3
"""Unit tests for GithubOrgClient class."""
import unittest
from unittest.mock import patch, PropertyMock, MagicMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient  # your class under test
from fixtures import TEST_PAYLOAD

class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")  # <- patch where get_json is used
    def test_org(self, org_name, mock_get_json):
        """Test that org method returns the expected organization data."""
        expected = {"login": org_name, "type": "Organization"}
        mock_get_json.return_value = expected

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
            )
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient _public_repos_url property."""
    def test_public_repos_url(self):
        """Test that _public_repos_url returns the correct URL."""
        test_payload = (
            {"repos_url": "https://api.github.com/orgs/testorg/repos"}
        )
        expected_url = "https://api.github.com/orgs/testorg/repos"

        with patch.object(
            GithubOrgClient, "org", new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = test_payload
            client = GithubOrgClient("testorg")
            result = client._public_repos_url
            self.assertEqual(result, expected_url)
            mock_org.assert_called_once()


if __name__ == "__main__":
    unittest.main(verbosity=2)


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient public_repos method."""
    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns a list of repository names."""
        fake_repos = [
            {"name": "repo1"},
            {"name": "repo2"},
        ]
        mock_get_json.return_value = fake_repos

        # Patch the _public_repos_url property
        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/testorg/repos"

            client = GithubOrgClient("testorg")
            repos = client.public_repos()

            self.assertEqual(repos, ["repo1", "repo2"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/testorg/repos"
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)

class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test GithubOrgClient.has_license with different license keys"""
        client = GithubOrgClient("any_org")  # org_name doesn't matter here
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)



@parameterized_class([
    {
        "org_payload": TEST_PAYLOAD["org_payload"],
        "repos_payload": TEST_PAYLOAD["repos_payload"],
        "expected_repos": TEST_PAYLOAD["expected_repos"],
        "apache2_repos": TEST_PAYLOAD["apache2_repos"],
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Start patching requests.get and set return values based on URL"""
        cls.get_patcher = patch("requests.get")

        mock_get = cls.get_patcher.start()
        # Setup side_effect to return different payloads based on the URL
        def side_effect(url):
            mock_response = MagicMock()
            if url.endswith("/orgs/google"):
                mock_response.json.return_value = cls.org_payload
            elif url.endswith("/orgs/google/repos"):
                mock_response.json.return_value = cls.repos_payload
            return mock_response

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop the patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns expected repo names"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test filtering repos by Apache-2.0 license"""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )

def test_public_repos(self):
    """
    Test that GithubOrgClient.public_repos returns the correct
    list of public repositories based on the repos_payload fixture.
    """
    client = GithubOrgClient("google")
    repos = client.public_repos()
    self.assertEqual(repos, self.expected_repos)


def test_public_repos_with_license(self):
    """
    Test that GithubOrgClient.public_repos filters repositories
    by the apache-2.0 license and returns the expected list.
    """
    client = GithubOrgClient("google")
    repos = client.public_repos(license="apache-2.0")
    self.assertEqual(repos, self.apache2_repos)