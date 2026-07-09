# Token Bucket Rate Limiter
A simple Python project that shows how the token bucket rate limiting idea works. It only uses the standard library.
## How It Works
Think of the bucket like a jar of tokens:
1. **Bucket** holds up to `capacity` tokens.
2. **Refill** adds tokens over time at `refill_rate` tokens per second, but never more than `capacity`.
3. **Request** tries to spend 1 token.
   - If there is a token left, the request is **allowed**.
   - If the bucket is empty, the request is **rejected**.
### Refill Formula
```
tokens_to_add = elapsed_seconds × refill_rate
new_token_count = min(capacity, current_tokens + tokens_to_add)
```
Example: if 2 seconds pass and `refill_rate = 1.5`, you get 3 new tokens, capped at `capacity`.
This lets you handle short bursts when the bucket is full, while still keeping a steady average rate over time.
## Project Structure
```
token_bucket_limiter/
├── token_bucket.py      # TokenBucket class
├── main.py              # Demo simulation
├── test_token_bucket.py # Unit tests
└── README.md
```
## Requirements
Python 3.9 or newer is recommended. Python 3.7+ should also work.

The `TokenBucket` class itself only uses the standard library. Running the test suite requires [pytest](https://docs.pytest.org/):
```bash
pip install pytest
```
## Running the Demo
Open a terminal in the `token_bucket_limiter` folder:
```bash
python main.py
```
### Example Output
```
Token Bucket Rate Limiter Demo
Capacity: 3, Refill rate: 1.0 token/sec
Request 1: ALLOWED (tokens remaining: 2.00)
Request 2: ALLOWED (tokens remaining: 1.00)
Request 3: ALLOWED (tokens remaining: 0.00)
Request 4: REJECTED (tokens remaining: 0.00)
Request 5: REJECTED (tokens remaining: 0.00)
Waiting 2 seconds for tokens to refill...
Request 6: ALLOWED (tokens remaining: 1.00)
Request 7: ALLOWED (tokens remaining: 0.00)
Request 8: REJECTED (tokens remaining: 0.00)
```
## Running Tests
```bash
python -m pytest -v
```
Or simply:
```bash
pytest
```
## Usage in Your Code
```python
from token_bucket import TokenBucket
limiter = TokenBucket(capacity=10, refill_rate=2.0)
if limiter.allow_request():
    print("Request allowed")
else:
    print("Rate limit exceeded")
```
