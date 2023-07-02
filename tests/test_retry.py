# tests/test_retry.py
import unittest
from tlescraper.utils import retry
from unittest.mock import MagicMock


class TestRetry(unittest.TestCase):
    def test_retry(self):
        function_inner = MagicMock(side_effect=[ValueError("Failure 1"), "Success"])

        @retry(max_retry=3, retry_interval=0.1)
        def test_function():
            return function_inner()

        test_function()
        self.assertEqual(function_inner.call_count, 2)

    def test_retry_success(self):
        function_inner = MagicMock(return_value="Success")

        @retry(max_retry=3, retry_interval=0.1)
        def test_function():
            return function_inner()

        result = test_function()
        self.assertEqual(result, "Success")
        self.assertEqual(function_inner.call_count, 1)

    def test_retry_fail(self):
        function_inner = MagicMock(side_effect=ValueError("Failure"))

        @retry(max_retry=3, retry_interval=0.1)
        def test_function():
            return function_inner()

        with self.assertRaises(Exception) as context:
            test_function()
        self.assertTrue("Failure" in str(context.exception))
        self.assertEqual(function_inner.call_count, 3)

    def test_retry_raise_on(self):
        function_inner = MagicMock(
            side_effect=[ZeroDivisionError(), ValueError("Failure 1")]
        )

        @retry(max_retry=3, retry_interval=0.1, raise_on=[ValueError])
        def test_function():
            return function_inner()

        with self.assertRaises(ValueError) as context:
            test_function()
        self.assertEqual(function_inner.call_count, 2)

    def test_retry_retry_on(self):
        function_inner = MagicMock(
            side_effect=[ZeroDivisionError(), ValueError("Failure 1")]
        )

        @retry(max_retry=3, retry_interval=0.1, retry_on=[ZeroDivisionError])
        def test_function():
            return function_inner()

        with self.assertRaises(ValueError) as context:
            test_function()
        self.assertEqual(function_inner.call_count, 2)


if __name__ == "__main__":
    unittest.main()
