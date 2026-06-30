"""Tests to make sure the rate limiter behaves the way we expect."""

import time
import unittest

from token_bucket import TokenBucket


class TestTokenBucket(unittest.TestCase):
    def test_initial_token_count(self) -> None:
        """A new bucket should start full."""
        bucket = TokenBucket(capacity=5, refill_rate=2.0)
        self.assertEqual(bucket.tokens, 5)
        self.assertEqual(bucket.capacity, 5)

    def test_token_consumption(self) -> None:
        """Each allowed request should use up one token."""
        bucket = TokenBucket(capacity=3, refill_rate=1.0)

        self.assertTrue(bucket.allow_request())
        self.assertAlmostEqual(bucket.tokens, 2, places=5)

        self.assertTrue(bucket.allow_request())
        self.assertAlmostEqual(bucket.tokens, 1, places=5)

    def test_token_refill_after_waiting(self) -> None:
        """Waiting should bring tokens back so another request can pass."""
        bucket = TokenBucket(capacity=2, refill_rate=1.0)

        bucket.allow_request()
        bucket.allow_request()
        self.assertAlmostEqual(bucket.tokens, 0, places=5)

        time.sleep(1.1)
        self.assertTrue(bucket.allow_request())

    def test_request_rejection_when_no_tokens(self) -> None:
        """Extra requests should get rejected when the bucket is empty."""
        bucket = TokenBucket(capacity=1, refill_rate=0.5)

        self.assertTrue(bucket.allow_request())
        self.assertFalse(bucket.allow_request())
        self.assertFalse(bucket.allow_request())


if __name__ == "__main__":
    unittest.main()
