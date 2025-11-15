#!/usr/bin/env python3
from unittest import TestCase
from unittest.mock import Mock , patch
from memoize import memoize
from mocking import get_json
from access_nested_map import access_nested_map
from parameterized import parameterized
from contextlib import contextmanager
import unittest

#Task 0 , 1
class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand([
        ({"a": 1} ,  ("a",) , 1),
        ({"a": {"b": 2}} , ("a",) , {"b": 2}),
        ({"a": {"b": 2}} , ("a","b") , 2 ),
    ])
    def test_access_nested_map(self , nested_map , path , expected):
        self.assertEqual(access_nested_map(nested_map , path) , expected)
    @parameterized.expand([
        ({} , ("a",)),
        ({"a": 1} , ("a","b")),
    ])
    def test_access_nested_map_exception(self , nested_map , path):
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map , path)
        self.assertEqual(str(cm.exception), f"'{path[-1]}'")

#Task 2
class TestGetJson(TestCase):
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('mocking.requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        # Create a Mock response object with json() method
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        # Set the return value of requests.get to our mock response
        mock_get.return_value = mock_response
        # Call the function
        result = get_json(test_url)
        # Assertions
        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)

#Task 3
class TestMemoize(TestCase):
    def test_memoize(self):
        class TestClass:
            def a_method(self):
                return 42
            @memoize
            def a_property(self):
                return self.a_method()
        # Patch a_method
        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            obj = TestClass()
            # Call property twice
            result1 = obj.a_property
            result2 = obj.a_property
            # Check results
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            # Ensure a_method was called ONLY once
            mock_method.assert_called_once()

if __name__ == "__main__" :
    unittest.main()