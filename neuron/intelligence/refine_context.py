from .axes import Axes
from typing import NamedTuple


class AxisRefinementContext(NamedTuple):
    model: str
    intent_summary: str
    search_space: Axes