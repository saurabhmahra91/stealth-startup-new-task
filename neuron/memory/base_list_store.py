from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from .config import valkey_client


T = TypeVar("T")


class ListStore(ABC, Generic[T]):
    def __init__(self, pk: str) -> None:
        self.pk = pk
        self._client = valkey_client

    def _key(self) -> str:
        return f"{self.prefix()}-{self.pk}"

    @abstractmethod
    def prefix(self) -> str: ...

    @abstractmethod
    def serialize(self, obj: T) -> str: ...

    @abstractmethod
    def deserialize(self, data: str) -> T: ...

    def save(self, item: T) -> None:
        self._client.rpush(self._key(), self.serialize(item))

    def get_all(self) -> list[T]:
        raw = self._client.lrange(self._key(), 0, -1)
        return [self.deserialize(item.decode("utf-8")) for item in raw]

    def latest(self) -> T | None:
        raw = self._client.lindex(self._key(), -1)
        if raw is None:
            return None
        return self.deserialize(raw.decode("utf-8"))

    def flush(self) -> None:
        self._client.delete(self._key())
