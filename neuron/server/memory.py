import os

import redis

valkey_client = redis.from_url(os.environ["REDIS_URL"])