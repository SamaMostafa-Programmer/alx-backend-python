#!/usr/bin/env python3
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


# -----------------------------
# 4. Parameterize and patch as decorators
# -----------------------------
class TestGithubOrgClient(unittest.TestCase):

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test GithubOrgClient.org returns correct value."""
        client = GithubOrgClient(org_name)
        client.org()
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")


# -----------------------------
# 5. Mocking a property
# -----------------------------
    def test_public_repos_url(self):
        """Test _public_repos_url property."""
        with patch.object(GithubOrgClient, "org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "https://api.github.com/orgs/test/repos"}
            client = GithubOrgClient("test")
            self.assertEqual(client._public_repos_url, "https://api.github.com/orgs/test/repos")


# -----------------------------
# 6. More patching
# -----------------------------
    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos method."""
        mock_get_json.return_value = [{"name": "repo1"}, {"name": "repo2"}]
        client = GithubOrgClient("test")
        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "fake_url"
            result = client.public_repos()
            self.assertEqual(result, ["repo1", "repo2"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with("fake_url")


# -----------------------------
# 7. Parameterize test_has_license
# -----------------------------
    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license method."""
        client = GithubOrgClient("test")
        self.assertEqual(client.has_license(repo, license_key), expected)


# -----------------------------
# 8 & 9. Integration test with fixtures
# -----------------------------
@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        # Define side_effect function based on URL
        def get_json_side_effect(url, *args, **kwargs):
            if url.endswith("/orgs/google"):
                mock_response = unittest.mock.Mock()
                mock_response.json.return_value = cls.org_payload
                return mock_response
            elif url.endswith("/orgs/google/repos"):
                mock_response = unittest.mock.Mock()
                mock_response.json.return_value = cls.repos_payload
                return mock_response
            return unittest.mock.Mock(json=lambda: {})

        cls.mock_get.side_effect = get_json_side_effect

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected repositories."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos filtered by license."""
        client = GithubOrgClient("google")
        result = client.public_repos(license="apache-2.0")
        self.assertEqual(result, self.apache2_repos)
