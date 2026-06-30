"""A small demo that sends a bunch of requests through the rate limiter."""

import time

from token_bucket import TokenBucket


def main() -> None:
    # Start with 3 tokens in the bucket, and add 1 new token every second
    bucket = TokenBucket(capacity=3, refill_rate=1.0)

    print("Token Bucket Rate Limiter Demo")
    print(f"Capacity: {bucket.capacity}, Refill rate: {bucket.refill_rate} token/sec\n")

    # Send 5 requests back to back. The first 3 should pass, then we run out.
    for i in range(1, 6):
        allowed = bucket.allow_request()
        status = "ALLOWED" if allowed else "REJECTED"
        print(f"Request {i}: {status} (tokens remaining: {bucket.tokens:.2f})")

    print("\nWaiting 2 seconds for tokens to refill...\n")
    time.sleep(2)

    # After the wait, we should have enough tokens for a couple more requests
    for i in range(6, 9):
        allowed = bucket.allow_request()
        status = "ALLOWED" if allowed else "REJECTED"
        print(f"Request {i}: {status} (tokens remaining: {bucket.tokens:.2f})")


if __name__ == "__main__":
    main()
