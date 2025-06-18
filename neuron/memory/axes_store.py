from .config import valkey_client
from ..intelligence.axes import Axes
from .base_list_store import ListStore


class AxesStore(ListStore[Axes]):
    def __init__(self, pk: str):
        super().__init__(pk)

    def prefix(self) -> str:
        return "axes"

    def serialize(self, obj: Axes) -> str:
        return obj.model_dump_json()

    def deserialize(self, data: str) -> Axes:
        return Axes.model_validate_json(data)
