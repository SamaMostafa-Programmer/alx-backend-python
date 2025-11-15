#!/usr/bin/env python3
"""Mocking helper for get_json function"""

import requests

def get_json(url):
    """Fetch JSON data from a URL"""
    response = requests.get(url)
    return response.json()
