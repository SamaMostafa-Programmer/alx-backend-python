#!/usr/bin/env python3
"""Client for Github API"""

import requests
from typing import List, Dict, Any
from mocking import get_json  # import from mocking.py عشان الـ patch يشتغل


class GithubOrgClient:
    """Github organization client"""

    def __init__(self, org_name: str):
        self.org_name = org_name

    @property
    def org(self) -> Dict[str, Any]:
        """Return the org JSON data"""
        return get_json(f"https://api.github.com/orgs/{self.org_name}")

    @property
    def _public_repos_url(self) -> str:
        """Return the URL for the public repos"""
        return self.org.get("repos_url")  # org property is already a dict

    def public_repos(self) -> List[str]:
        """Return the list of public repo names"""
        repos = get_json(self._public_repos_url)
        return [repo["name"] for repo in repos]

    @staticmethod
    def has_license(repo: Dict[str, Any], license_key: str) -> bool:
        """Check if a repo has a specific license"""
        license_info = repo.get("license")
        if license_info:
            return license_info.get("key") == license_key
        return False
