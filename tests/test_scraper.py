import os
import unittest
from unittest import mock
from tlescraper.scraper import save_tle, get_tle, CERESTRACK_BASE_URL
from urllib.error import URLError

OUTPUT_DIR = "./output"


class TestSaveTle(unittest.TestCase):
    @mock.patch("tlescraper.scraper.urlopen")
    def test_get_tle(self, mock_urlopen):
        test_CATNR = "12345"
        expected_content = "TLE Line1\nTLE Line2\nTLE Line3\n"

        # Mock the response from urlopen
        mock_response = mock.Mock()
        mock_response.read.return_value = expected_content.encode("utf-8")
        mock_urlopen.return_value = mock_response

        result = get_tle(test_CATNR)

        # Check if the function calls are correct
        mock_urlopen.assert_called_once_with(
            f"{CERESTRACK_BASE_URL}/gp.php?CATNR={test_CATNR}"
        )
        self.assertEqual(result, expected_content)

    @mock.patch("tlescraper.scraper.urlopen")
    def test_get_tle_failure(self, mock_urlopen):
        test_CATNR = "12345"
        expected_content = "TLE Line1\nTLE Line2\nTLE Line3\n"

        # Mock the response from urlopen
        mock_response = mock.Mock()
        mock_response.read.return_value = expected_content.encode("utf-8")
        mock_urlopen.side_effect = [URLError("404"), mock_response]

        result = get_tle(test_CATNR)

        # Check if the function calls are correct
        self.assertEqual(mock_urlopen.call_count, 2)
        self.assertEqual(result, expected_content)

    @mock.patch("tlescraper.scraper.urlopen")
    def test_get_tle_one_line(self, mock_urlopen):
        test_CATNR = "12345"
        expected_content = "TLE Line1"

        # Mock the response from urlopen
        mock_response = mock.Mock()
        mock_response.read.return_value = expected_content.encode("utf-8")
        mock_urlopen.return_value = mock_response

        with self.assertRaises(Exception) as context:
            get_tle(test_CATNR)

        # Check if the function calls are correct
        self.assertTrue(
            f"Error loading {CERESTRACK_BASE_URL}/gp.php?CATNR={test_CATNR}: {expected_content}"
            in str(context.exception)
        )

    @mock.patch("tlescraper.scraper.get_tle")
    @mock.patch("os.makedirs")
    @mock.patch("os.path.exists")
    @mock.patch("builtins.open", new_callable=mock.mock_open())
    def test_save_tle_success(
        self, mock_open, mock_os_exists, mock_os_makedirs, mock_scraper
    ):
        mock_os_exists.return_value = False

        test_CATNR = "12345"
        test_content = "TLE Line1\nTLE Line2\nTLE Line3\n"
        expected_filename = os.path.join(OUTPUT_DIR, f"{test_CATNR}.txt")

        # Mock the response from urlopen
        mock_scraper.return_value = test_content

        result = save_tle(test_CATNR, OUTPUT_DIR)

        # Check if the function calls are correct
        mock_scraper.assert_called_once_with(test_CATNR)
        mock_os_makedirs.assert_called_once_with(os.path.dirname(expected_filename))
        mock_open.assert_called_once_with(expected_filename, "w", encoding="ascii")

        self.assertEqual(result, test_content)

    @mock.patch("tlescraper.scraper.get_tle")
    @mock.patch("os.makedirs")
    @mock.patch("os.path.exists")
    @mock.patch("builtins.open", new_callable=mock.mock_open())
    def test_save_tle_faliure(
        self, mock_open, mock_os_exists, mock_os_makedirs, mock_scraper
    ):
        mock_os_exists.return_value = False
        test_CATNR = "12345"

        # Mock the response from urlopen
        mock_scraper.side_effect = URLError("404")

        with self.assertRaises(Exception) as context:
            save_tle(test_CATNR, OUTPUT_DIR)

        # Check if the function not called
        mock_scraper.assert_called_once_with(test_CATNR)
        mock_os_makedirs.asset_not_called()
        mock_open.assert_not_called()


if __name__ == "__main__":
    unittest.main()
