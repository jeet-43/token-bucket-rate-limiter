"""Unit tests for the token bucket rate limiter."""

import pytest

from token_bucket import TokenBucket


def test_init_sets_starting_tokens_to_capacity():
    bucket = TokenBucket(capacity=5, refill_rate=1.0)
    assert bucket.tokens == 5
    assert bucket.capacity == 5
    assert bucket.refill_rate == 1.0


def test_init_rejects_non_positive_capacity():
    with pytest.raises(ValueError):
        TokenBucket(capacity=0, refill_rate=1.0)
    with pytest.raises(ValueError):
        TokenBucket(capacity=-1, refill_rate=1.0)


def test_init_rejects_negative_refill_rate():
    with pytest.raises(ValueError):
        TokenBucket(capacity=5, refill_rate=-1.0)


def test_allow_request_consumes_one_token_per_call():
    bucket = TokenBucket(capacity=3, refill_rate=0.0)
    assert bucket.allow_request() is True
    assert bucket.tokens == pytest.approx(2)
    assert bucket.allow_request() is True
    assert bucket.tokens == pytest.approx(1)


def test_allow_request_rejects_when_bucket_is_empty():
    bucket = TokenBucket(capacity=1, refill_rate=0.0)
    assert bucket.allow_request() is True
    assert bucket.allow_request() is False


def test_refill_adds_tokens_based_on_elapsed_time(monkeypatch):
    fake_time = [100.0]
    monkeypatch.setattr("time.monotonic", lambda: fake_time[0])

    bucket = TokenBucket(capacity=5, refill_rate=2.0)
    bucket.tokens = 0.0

    fake_time[0] += 1.5  # 1.5 seconds at 2 tokens/sec -> 3 tokens added
    bucket._refill()

    assert bucket.tokens == pytest.approx(3.0)


def test_refill_does_not_exceed_capacity(monkeypatch):
    fake_time = [100.0]
    monkeypatch.setattr("time.monotonic", lambda: fake_time[0])

    bucket = TokenBucket(capacity=3, refill_rate=5.0)
    bucket.tokens = 2.5

    fake_time[0] += 10  # plenty of time to overflow the bucket
    bucket._refill()

    assert bucket.tokens == 3


def test_repr_includes_key_fields():
    bucket = TokenBucket(capacity=3, refill_rate=1.0)
    text = repr(bucket)
    assert "capacity=3" in text
    assert "refill_rate=1.0" in text
    assert "tokens=3.00" in text
