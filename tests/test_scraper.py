import os
import ssl
import unittest
from unittest import mock
from tlescraper.scraper import save_tle, get_tle, CELESTRAK_BASE_URL
from urllib.error import URLError

OUTPUT_DIR = "./output"


def _make_mock_response(content: str):
    """urlopen context manager として動作するモックを返す"""
    mock_response = mock.MagicMock()
    mock_response.read.return_value = content.encode("utf-8")
    mock_response.__enter__.return_value = mock_response
    return mock_response


class TestSaveTle(unittest.TestCase):
    @mock.patch("tlescraper.scraper.urlopen")
    def test_get_tle(self, mock_urlopen):
        test_CATNR = "12345"
        expected_content = "TLE Line1\nTLE Line2\nTLE Line3\n"

        mock_urlopen.return_value = _make_mock_response(expected_content)

        result = get_tle(test_CATNR)

        mock_urlopen.assert_called_once_with(
            f"{CELESTRAK_BASE_URL}/gp.php?CATNR={test_CATNR}",
            context=mock.ANY,
        )
        ssl_ctx = mock_urlopen.call_args.kwargs["context"]
        self.assertEqual(ssl_ctx.verify_mode, ssl.CERT_NONE)
        self.assertFalse(ssl_ctx.check_hostname)
        self.assertEqual(result, expected_content)

    @mock.patch("tlescraper.scraper.urlopen")
    def test_get_tle_failure(self, mock_urlopen):
        test_CATNR = "12345"
        expected_content = "TLE Line1\nTLE Line2\nTLE Line3\n"

        mock_urlopen.side_effect = [URLError("404"), _make_mock_response(expected_content)]

        result = get_tle(test_CATNR)

        self.assertEqual(mock_urlopen.call_count, 2)
        self.assertEqual(result, expected_content)

    @mock.patch("tlescraper.scraper.urlopen")
    def test_get_tle_one_line(self, mock_urlopen):
        test_CATNR = "12345"
        expected_content = "TLE Line1"

        mock_urlopen.return_value = _make_mock_response(expected_content)

        with self.assertRaises(ValueError) as context:
            get_tle(test_CATNR)

        self.assertEqual(mock_urlopen.call_count, 1)
        self.assertTrue(
            f"Error loading {CELESTRAK_BASE_URL}/gp.php?CATNR={test_CATNR}: {expected_content}"
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

        mock_scraper.return_value = test_content

        result = save_tle(test_CATNR, OUTPUT_DIR)

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

        mock_scraper.side_effect = URLError("404")

        with self.assertRaises(Exception) as _:
            save_tle(test_CATNR, OUTPUT_DIR)

        mock_scraper.assert_called_once_with(test_CATNR)
        mock_os_makedirs.asset_not_called()
        mock_open.assert_not_called()


if __name__ == "__main__":
    unittest.main()
