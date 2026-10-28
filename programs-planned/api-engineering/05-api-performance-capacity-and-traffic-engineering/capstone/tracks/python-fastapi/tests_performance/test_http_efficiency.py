from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from api_performance.http_efficiency import (
    HTTPPolicyError,
    RangeNotSatisfiable,
    choose_content_encoding,
    content_chunks,
    if_none_match_matches,
    if_range_allows_range,
    parse_single_range,
    strong_match,
    weak_match,
)
from api_performance.streaming import (
    estimated_application_buffer_bytes,
    iter_file_range,
)


class ValidatorTests(unittest.TestCase):
    def test_weak_and_strong_matching(self) -> None:
        self.assertTrue(weak_match('W/"abc"', '"abc"'))
        self.assertFalse(strong_match('W/"abc"', '"abc"'))
        self.assertTrue(strong_match('"abc"', '"abc"'))

    def test_if_none_match(self) -> None:
        self.assertTrue(if_none_match_matches('"x", W/"abc"', '"abc"'))
        self.assertTrue(if_none_match_matches("*", '"abc"'))
        self.assertFalse(if_none_match_matches('"x"', '"abc"'))

    def test_if_range_requires_strong(self) -> None:
        self.assertTrue(if_range_allows_range('"abc"', '"abc"'))
        self.assertFalse(if_range_allows_range('W/"abc"', '"abc"'))

    def test_malformed_tag_rejected(self) -> None:
        with self.assertRaises(HTTPPolicyError):
            if_none_match_matches("abc", '"abc"')


class RangeTests(unittest.TestCase):
    def test_fixed_range(self) -> None:
        selection = parse_single_range("bytes=100-199", 1000)
        self.assertEqual(selection.start, 100)
        self.assertEqual(selection.end_exclusive, 200)
        self.assertEqual(selection.length, 100)
        self.assertEqual(selection.content_range, "bytes 100-199/1000")

    def test_open_range(self) -> None:
        selection = parse_single_range("bytes=900-", 1000)
        self.assertEqual(selection.length, 100)

    def test_suffix_range(self) -> None:
        selection = parse_single_range("bytes=-200", 1000)
        self.assertEqual((selection.start, selection.end_exclusive), (800, 1000))

    def test_unsatisfied(self) -> None:
        with self.assertRaises(RangeNotSatisfiable) as caught:
            parse_single_range("bytes=1500-", 1000)
        self.assertEqual(str(caught.exception), "bytes */1000")

    def test_multi_range_rejected(self) -> None:
        with self.assertRaises(HTTPPolicyError):
            parse_single_range("bytes=0-1,5-6", 10)

    def test_chunks_exact(self) -> None:
        data = b"0123456789"
        self.assertEqual(
            b"".join(content_chunks(data, start=2, length=5, chunk_size=2)),
            b"23456",
        )


class StreamingTests(unittest.TestCase):
    def test_file_range(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "object.bin"
            path.write_bytes(b"abcdefghij")
            self.assertEqual(
                b"".join(iter_file_range(path, start=3, length=4, chunk_size=2)),
                b"defg",
            )

    def test_buffer_estimate(self) -> None:
        self.assertEqual(
            estimated_application_buffer_bytes(
                active_streams=200,
                chunk_size=64 * 1024,
                buffers_per_stream=2,
            ),
            25 * 1024 * 1024,
        )

    def test_compression_policy(self) -> None:
        self.assertEqual(
            choose_content_encoding(
                accept_encoding="gzip, br",
                media_type="application/json",
                body_length=5000,
            ),
            "gzip",
        )
        self.assertEqual(
            choose_content_encoding(
                accept_encoding="gzip",
                media_type="application/octet-stream",
                body_length=5000,
            ),
            "identity",
        )
        self.assertEqual(
            choose_content_encoding(
                accept_encoding="gzip",
                media_type="application/json",
                body_length=5000,
                range_requested=True,
            ),
            "identity",
        )


if __name__ == "__main__":
    unittest.main()
