import json
from typing import Any

from .config import valkey_client
from .base_list_store import ListStore


class ConversationStore(ListStore[dict[str, Any]]):
    def __init__(self, pk: str) -> None:
        super().__init__(pk)

    def prefix(self) -> str:
        return "conv"

    def serialize(self, obj: dict[str, Any]) -> str:
        return json.dumps(obj)

    def deserialize(self, data: str) -> dict[str, Any]:
        return json.loads(data)

    def _blob_key(self) -> str:
        return self.pk

    def exists(self) -> bool:
        return self._client.exists(self._blob_key()) == 1

    def flush(self) -> None:
        self._client.delete(self._key())
        self._client.delete(self._blob_key())

    def get_chat_history(self) -> list[dict[str, Any]]:
        if self.exists():
            raw = self._client.get(self._blob_key())
            return json.loads(raw)
        return []

    def save_chat_history(self, history: list[dict[str, Any]]) -> None:
        self._client.set(self._blob_key(), json.dumps(history), ex=60 * 60 * 24)

    def get_last_user_content(self) -> str | None:
        """
        Returns the content of the last message from the user.
        """
        conv = self.get_all()
        for msg in reversed(conv):
            if msg.get("role") == "user":
                return msg.get("content")
        return None

    def format_chat_prompt(self) -> str:
        """
        Returns a formatted string version of the conversation history.
        """
        messages = self.get_all()
        prompt = []
        for msg in messages:
            role = msg.get("role", "").capitalize()
            content = msg.get("content", "").strip()
            content = content.split("</justification>")[-1].strip()
            prompt.append(f"{role}: {content}")
        return "\n".join(prompt)
