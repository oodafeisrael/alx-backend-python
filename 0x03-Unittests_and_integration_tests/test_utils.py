#!/usr/bin/env python3
"""Unit test for access_nested_map"""
import unittest
from parameterized import parameterized
from utils import access_nested_map
from utils import get_json
from unittest.mock import patch, Mock
from utils import memoize


class TestAccessNestedMap(unittest.TestCase):
    """Test class for access_nested_map"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map returns expected result"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test access_nested_map raises KeyError with invalid paths"""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), repr(path[-1]))


class TestGetJson(unittest.TestCase):
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch("utils.requests.get")
    def test_get_json(self, test_url, test_payload, mock_get):
        """
        Test that get_json returns the correct
        payload and makes one call to requests.get
        """
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        result = get_json(test_url)

        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    def test_memoize(self):
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(
            TestClass, "a_method", return_value=42
        ) as mock_method:
            test_obj = TestClass()

            # Call the memoized property twice
            result1 = test_obj.a_property
            result2 = test_obj.a_property

            # Assert method was called only once
            mock_method.assert_called_once()

            # Assert result is correct and same in both calls
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
