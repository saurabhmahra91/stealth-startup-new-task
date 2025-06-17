import json
import os

import redis

valkey_client = redis.from_url(os.environ["REDIS_URL"])


def get_chat_history(user_id):
    key = user_id

    if valkey_client.exists(key):
        res = valkey_client.get(key)
        return json.loads(res)
    else:
        return []


def save_chat_history(user_id, history):
    key = user_id
    valkey_client.set(key, json.dumps(history), ex=60 * 60 * 24)


def user_exists(user_id):
    return valkey_client.exists(user_id) == 1


def flush_user_memory(user_id):
    valkey_client.delete(user_id)


def get_user_conversation(user_id: str) -> list[dict]:
    """
    Fetches the full conversation history for a given user_id.
    Assumes messages are stored as JSON strings in a Redis list.
    """
    key = user_id
    messages = valkey_client.lrange(key, 0, -1)  # Get all messages
    if not messages:
        return []

    return [json.loads(m.decode("utf-8")) for m in messages]


def store_user_message(user_id: str, role: str, content: str) -> None:
    """
    Stores a single message in the user's Redis conversation list.
    `role` should be either "user" or "assistant".
    """
    key = user_id
    message = {"role": role, "content": content}
    valkey_client.rpush(key, json.dumps(message))
