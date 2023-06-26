import os
import unittest
from unittest import mock
from tlescraper.scraper import save_tle, CERESTRACK_BASE_URL

OUTPUT_DIR = "./output"


class TestSaveTle(unittest.TestCase):
    @mock.patch("urllib.request.urlopen")
    @mock.patch("os.makedirs")
    @mock.patch("os.path.exists")
    @mock.patch("builtins.open", new_callable=mock.mock_open())
    def test_save_tle_success(
        self, mock_open, mock_os_exists, mock_os_makedirs, mock_urlopen
    ):
        mock_os_exists.return_value = False

        test_CATNR = "12345"
        expected_content = "TLE Line1\nTLE Line2\nTLE Line3\n"
        expected_filename = os.path.join(OUTPUT_DIR, f"{test_CATNR}.txt")

        # Mock the response from urlopen
        mock_response = mock.Mock()
        mock_response.getcode.return_value = 200
        mock_response.read.return_value = expected_content.encode("utf-8")
        mock_urlopen.return_value = mock_response

        result = save_tle(test_CATNR, OUTPUT_DIR)

        # Check if the function calls are correct
        mock_urlopen.assert_called_once_with(
            f"{CERESTRACK_BASE_URL}/gp.php?CATNR={test_CATNR}"
        )
        mock_os_makedirs.assert_called_once_with(os.path.dirname(expected_filename))
        mock_open.assert_called_once_with(expected_filename, "w", encoding="ascii")

        self.assertEqual(result, expected_content.strip())

    @mock.patch("urllib.request.urlopen")
    def test_save_tle_failed(self, mock_urlopen):
        test_CATNR = "12345"

        # Mock the response from urlopen
        mock_response = mock.Mock()
        mock_response.getcode.return_value = 404
        mock_urlopen.return_value = mock_response

        with self.assertRaises(Exception) as context:
            save_tle(test_CATNR, OUTPUT_DIR)

        self.assertTrue(
            f"Error loading {CERESTRACK_BASE_URL}/gp.php?CATNR={test_CATNR}: 404"
            in str(context.exception)
        )


if __name__ == "__main__":
    unittest.main()
