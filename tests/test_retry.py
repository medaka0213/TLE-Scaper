# tests/test_retry.py
import unittest
from tlescraper.utils import retry
from unittest.mock import MagicMock


class TestRetry(unittest.TestCase):
    def test_retry(self):
        function_inner = MagicMock(side_effect=[ValueError("Failure 1"), "Success"])

        @retry(max_retry=3, retry_interval=0.1)
        def failing_function():
            return function_inner()

        failing_function()
        self.assertEqual(function_inner.call_count, 2)

    def test_retry_success(self):
        function_inner = MagicMock(return_value="Success")

        @retry(max_retry=3, retry_interval=0.1)
        def successful_function():
            return function_inner()

        result = successful_function()
        self.assertEqual(result, "Success")
        self.assertEqual(function_inner.call_count, 1)

    def test_retry_fail(self):
        function_inner = MagicMock(side_effect=ValueError("Failure"))

        @retry(max_retry=3, retry_interval=0.1)
        def failing_function():
            return function_inner()

        with self.assertRaises(Exception) as context:
            failing_function()
        self.assertTrue("Failure" in str(context.exception))
        self.assertEqual(function_inner.call_count, 3)


if __name__ == "__main__":
    unittest.main()
