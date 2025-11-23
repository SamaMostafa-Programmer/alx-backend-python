#!/usr/bin/env python3
"""Module to make HTTP GET requests and return JSON payloads."""
import requests

def get_json(url):
    """Make a GET request to a URL and return its JSON payload.

    Args:
        url (str): The URL to request.

    Returns:
        dict: JSON response content.
    """
    return requests.get(url).json()
