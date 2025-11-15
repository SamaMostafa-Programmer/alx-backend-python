#!/usr/bin/env python3
"""Unit tests for client.py"""

import unittest
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized, parameterized_class

from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that org returns correct value"""
        mock_get_json.return_value = {"login": org_name}
        client = GithubOrgClient(org_name)
        result = client.org
        self.assertEqual(result, {"login": org_name})
        mock_get_json.assert_called_once()


class TestGithubOrgClientProperty(unittest.TestCase):
    """Test GithubOrgClient._public_repos_url property"""

    def test_public_repos_url(self):
        """Test that _public_repos_url returns correct URL"""
        client = GithubOrgClient("google")

        with patch.object(
            GithubOrgClient, "org", new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/google/repos"
            }

            self.assertEqual(
                client._public_repos_url,
                "https://api.github.com/orgs/google/repos"
            )


class TestGithubOrgClientMethods(unittest.TestCase):
    """Test GithubOrgClient methods"""

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns correct list"""
        client = GithubOrgClient("google")
        mock_get_json.return_value = [{"name": "repo1"}, {"name": "repo2"}]

        with patch.object(
            GithubOrgClient, "_public_repos_url", new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/google/repos"
            repos = client.public_repos()
            self.assertEqual(repos, ["repo1", "repo2"])
            mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns correct bool"""
        client = GithubOrgClient("google")
        self.assertEqual(client.has_license(repo, license_key), expected)


@parameterized_class([{
    "org_payload": org_payload,
    "repos_payload": repos_payload,
    "expected_repos": expected_repos,
    "apache2_repos": apache2_repos
}])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient"""

    @classmethod
    def setUpClass(cls):
        """Setup class-level patching"""
        cls.get_patcher = patch("client.requests.get")
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url, *args, **kwargs):
            if url == cls.org_payload["repos_url"]:
                mock_resp = Mock()
                mock_resp.json.return_value = cls.repos_payload
                return mock_resp
            mock_resp = Mock()
            mock_resp.json.return_value = cls.org_payload
            return mock_resp

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop class-level patching"""
        cls.get_patcher.stop()


if __name__ == "__main__":
    unittest.main()
