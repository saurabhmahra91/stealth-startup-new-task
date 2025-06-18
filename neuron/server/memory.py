import json
import os
from ..intelligence.axes import Axes

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
    messages = valkey_client.lrange(get_key_for_conversation(user_id), 0, -1)  # Get all messages
    if not messages:
        return []

    return [json.loads(m.decode("utf-8")) for m in messages]


def store_user_message(user_id: str, role: str, content: str) -> None:
    """
    Stores a single message in the user's Redis conversation list.
    `role` should be either "user" or "assistant".
    """
    message = {"role": role, "content": content}
    valkey_client.rpush(get_key_for_conversation(user_id), json.dumps(message))


def get_key_for_conversation(user_id: str):
    return user_id


def get_key_for_user_axes(user_id: str):
    return f"axes-{user_id}"


def save_user_axes(user_id: str, axes: Axes) -> None:
    """
    Serializes and stores the Axes object for a user.
    """
    valkey_client.set(get_key_for_user_axes(user_id), axes.model_dump_json(), ex=60 * 60 * 24)  # optional TTL


def get_user_axes(user_id: str) -> Axes | None:
    """
    Retrieves and deserializes the Axes object for a user.
    Returns None if not found.
    """
    raw_data = valkey_client.get(get_key_for_user_axes(user_id))
    if raw_data is None:
        return None
    return Axes.model_validate_json(raw_data)
