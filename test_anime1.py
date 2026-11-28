import json
import unittest
from unittest.mock import patch

import requests

import anime1


class AnimeListFetchTest(unittest.TestCase):
    @staticmethod
    def response(status, body=b"[]"):
        result = requests.Response()
        result.status_code = status
        result.url = anime1.ANIME_LIST_URL
        result._content = body
        return result

    @patch("anime1.sleep")
    @patch("anime1.requests.get")
    def test_521_retries_then_parses_success(self, get, sleep):
        get.side_effect = [self.response(521), self.response(200, b"[[1]]")]
        self.assertEqual(anime1.fetch_anime_list(), [[1]])
        self.assertEqual(get.call_count, 2)
        get.assert_called_with(anime1.ANIME_LIST_URL, headers=anime1.headers, timeout=(5, 30))
        sleep.assert_called_once_with(1)

    @patch("anime1.sleep")
    @patch("anime1.requests.get")
    def test_repeated_521_remains_failure(self, get, sleep):
        get.return_value = self.response(521)
        with self.assertRaises(requests.exceptions.HTTPError):
            anime1.fetch_anime_list()
        self.assertEqual(get.call_count, 3)
        self.assertEqual([entry.args for entry in sleep.call_args_list], [(1,), (2,)])

    @patch("anime1.sleep")
    @patch("anime1.requests.get")
    def test_timeout_retries(self, get, sleep):
        get.side_effect = [requests.exceptions.Timeout(), self.response(200)]
        self.assertEqual(anime1.fetch_anime_list(), [])
        self.assertEqual(get.call_count, 2)

    @patch("anime1.sleep")
    @patch("anime1.requests.get")
    def test_permanent_errors_and_invalid_payload_do_not_retry(self, get, sleep):
        for response, error_type in [
            (self.response(403), requests.exceptions.HTTPError),
            (requests.exceptions.SSLError(), requests.exceptions.SSLError),
            (self.response(200, b"<html>"), json.JSONDecodeError),
        ]:
            with self.subTest(error=error_type):
                get.reset_mock()
                get.side_effect = [response]
                with self.assertRaises(error_type):
                    anime1.fetch_anime_list()
                get.assert_called_once()
        sleep.assert_not_called()


if __name__ == "__main__":
    unittest.main()
