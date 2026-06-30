"""A simple token bucket rate limiter."""

import time


class TokenBucket:
    """Controls how many requests can go through by spending and refilling tokens."""

    def __init__(self, capacity: float, refill_rate: float) -> None:
        """
        Set up a new bucket.

        capacity: the most tokens we can store at once
        refill_rate: how many tokens come back each second
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill_time = time.monotonic()

    def _refill(self) -> None:
        """Top up the bucket based on how long it has been since we last checked."""
        now = time.monotonic()
        elapsed = now - self.last_refill_time

        # More time passed means more tokens. Example: 2 seconds at 1.5/sec gives 3 tokens.
        tokens_to_add = elapsed * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill_time = now

    def allow_request(self) -> bool:
        """
        Check if one request can go through.

        We refill first, then try to spend one token.
        Returns True when the request is allowed, False when we are out of tokens.
        """
        self._refill()

        if self.tokens >= 1:
            self.tokens -= 1
            return True

        return False
