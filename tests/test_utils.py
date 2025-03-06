# =============================================================================
# Modules
# =============================================================================

# Python modules
import os
import requests
import unittest
from unittest.mock import patch, MagicMock
from utils import (
    get_env_var,
    get_news_api_endpoint,
    get_http_response,
    get_article_title_description_link,
)

# =============================================================================
# Tests
# =============================================================================

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.patcher_logger = patch("utils.logger")
        self.mock_logger = self.patcher_logger.start()

    def tearDown(self):
        self.patcher_logger.stop()


class TestGetEnvVar(BaseTestCase):
    @patch("os.getenv")
    def test_get_env_var_success(self, mock_getenv):
        mock_getenv.return_value = "test_value"
        result = get_env_var("TEST_VAR")
        self.assertEqual(result, "test_value")
        self.mock_logger.info.assert_called()

    @patch("os.getenv", return_value=None)
    def test_get_env_var_not_found(self, mock_getenv):
        result = get_env_var("MISSING_VAR")
        self.assertIsNone(result)
        self.mock_logger.info.assert_called()


class TestGetNewsApiEndpoint(BaseTestCase):
    def test_get_news_api_endpoint(self):
        api_key = "test_api_key"
        topic = "climate"
        expected_url = "https://newsapi.org/v2/everything?q=climate&from=2025-02-06&sortBy=publishedAt&language=en&apiKey=test_api_key"
        result = get_news_api_endpoint(api_key, topic)
        self.assertEqual(result, expected_url)
        self.mock_logger.debug.assert_called()


class TestGetHttpResponse(BaseTestCase):
    @patch("utils.requests.get")
    def test_get_http_response_success(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"status": "ok"}
        mock_requests_get.return_value = mock_response

        url = "http://example.com"
        headers = {"User-Agent": "test-agent"}
        result = get_http_response(url, headers)

        self.assertEqual(result, {"status": "ok"})
        self.mock_logger.info.assert_called()

    @patch("utils.requests.get", side_effect=requests.exceptions.RequestException("Request failed"))
    def test_get_http_response_request_exception(self, mock_requests_get):
        url = "http://example.com"
        headers = {"User-Agent": "test-agent"}
        with self.assertRaises(requests.exceptions.RequestException):
            get_http_response(url, headers)
        self.mock_logger.error.assert_called()


class TestGetArticleTitleDescriptionLink(BaseTestCase):
    def test_get_article_title_description_link_success(self):
        content = {
            "articles": [
                {"title": "Title 1", "description": "Desc 1", "url": "http://link1.com"},
                {"title": "Title 2", "description": "Desc 2", "url": "http://link2.com"},
            ]
        }
        expected_output = """[1]\nTitle: Title 1\nDescription: Desc 1\nLink: http://link1.com\n\n[2]\nTitle: Title 2\nDescription: Desc 2\nLink: http://link2.com"""
        result = get_article_title_description_link(content)
        self.assertEqual(result, expected_output)
        self.mock_logger.info.assert_called()

    def test_get_article_title_description_link_missing_key(self):
        content = {}
        with self.assertRaises(ValueError):
            get_article_title_description_link(content)
        self.mock_logger.error.assert_called()


if __name__ == "__main__":
    unittest.main()
