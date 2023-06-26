import unittest
from unittest.mock import patch, mock_open
from tlescraper import render


class TestHtmlRender(unittest.TestCase):
    @patch("os.walk")
    def test_search_files(self, mock_os_walk):
        mock_os_walk.return_value = [
            (".", ("dir1",), ("file1.txt", "file2.txt")),
            ("./dir1", (), ("file3.txt",)),
        ]
        expected = ["file1.txt", "file2.txt", "dir1/file3.txt"]
        self.assertEqual(render.search_files("."), expected)

    @patch("tlescraper.render.Environment")
    def test_render_files(self, mock_jinja_env):
        mock_template = mock_jinja_env.return_value.get_template.return_value
        mock_template.render.return_value = "rendered template"
        mock_os_path_exists = patch("os.path.exists", return_value=False).start()
        mock_os_makedirs = patch("os.makedirs").start()
        mock_open_func = mock_open()

        with patch("builtins.open", mock_open_func):
            result = render.render_files(
                "templates/index.html.j2",
                "output/index.html",
                files=["file1.txt", "file2.txt", "dir1/file3.txt"],
            )

        mock_os_path_exists.assert_called_once_with("output")
        mock_os_makedirs.assert_called_once_with("output")
        mock_open_func.assert_called_once_with("output/index.html", "w")
        handle = mock_open_func()
        handle.write.assert_called_once_with("rendered template")
        self.assertEqual(result, "rendered template")

    @patch(
        "tlescraper.render.search_files",
        return_value=["file1.txt", "file2.txt", "dir1/file3.txt"],
    )
    @patch("tlescraper.render.render_files", return_value="rendered template")
    def test_generate_index_html(self, mock_render_files, mock_search_files):
        result = render.generate_index_html(".")
        mock_search_files.assert_called_once_with(".")
        mock_render_files.assert_called_once_with(
            "templates/index.html.j2",
            "./index.html",
            files=["file1.txt", "file2.txt", "dir1/file3.txt"],
        )
        self.assertEqual(result, "rendered template")


if __name__ == "__main__":
    unittest.main()
