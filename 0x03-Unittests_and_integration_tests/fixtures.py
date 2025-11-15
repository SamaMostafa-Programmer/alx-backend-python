# fixtures.py
"""Fixtures for GithubOrgClient integration tests."""

# Example organization payload
org_payload = {
    "login": "google",
    "id": 123456,
    "repos_url": "https://api.github.com/orgs/google/repos"
}

# Example repositories payload returned by the API
repos_payload = [
    {"name": "repo1", "license": {"key": "apache-2.0"}},
    {"name": "repo2", "license": {"key": "mit"}},
    {"name": "repo3", "license": {"key": "apache-2.0"}}
]

# Expected list of repository names for org_payload and repos_payload
expected_repos = ["repo1", "repo2", "repo3"]

# Repositories with apache-2.0 license only
apache2_repos = ["repo1", "repo3"]
