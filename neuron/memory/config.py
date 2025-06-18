import os
import logging
import redis

valkey_client = redis.from_url(os.environ["REDIS_URL"])
logger = logging.getLogger(__name__)


def test_valkey():
    try:
        # Ping server
        pong = valkey_client.ping()
        logger.info("PONG? %s", pong)

        # Set a key
        valkey_client.set("test_key", "valkey_rocks")

        # Get the key
        value = valkey_client.get("test_key")
        logger.info("Value for 'test_key': %s", value)

        # Delete the key
        valkey_client.delete("test_key")

        logger.info("Valkey test passed!")

    except Exception as e:
        print(f"Error connecting or running commands: {e}")
