import os

from crewai.flow import router
from crewai.flow.flow import Flow, and_, listen, or_, start
from pydantic import BaseModel

from ..search.explicit import filter_explicit
from ..search.implicit.feature_presence import get_sorted_skus_by_soft_score
from ..search.utils import load_fashion_data
from .axes import Axes
from .decision import route_query
from .followup import _ask_followup
from .justification import _justify
from .refinement_v2 import _refine_axes


def get_followup_axes():
    return Axes.model_json_schema()


class SearchState(BaseModel):
    conversation: list[dict] = []
    skus: list[dict] = load_fashion_data()
    search_space: Axes = Axes()
    justification: str = ""
    followup: str = ""


class SearchFlow(Flow[SearchState]):
    model = os.environ.get("MODEL", "ollama/gemma3:4b")

    @start()
    def receive_user_query(self):
        print(self.state)

    @listen(receive_user_query)
    def ask_followup(self):
        result = _ask_followup(model=self.model, conv=self.state.conversation, search_space=self.state.search_space)
        self.state.followup = result
        print("The followup question asked = ", result)
        return

    @router(receive_user_query)
    def should_refine_search(self):
        should_refine = route_query(self.model, self.state.conversation)
        if should_refine:
            return "SHOULD_REFINE_SEARCH"
        else:
            return "SHOULD_NOT_REFINE_SEARCH"

    @listen("SHOULD_REFINE_SEARCH")
    def begin_preparing_nonempty_justification(self):
        return

    @listen("SHOULD_NOT_REFINE_SEARCH")
    def begin_preparing_empty_justification(self):
        self.state.justification = ""
        return

    @listen(begin_preparing_nonempty_justification)
    async def get_axes_preferences(self):
        self.state.search_space = await _refine_axes(
            self.model, search_space=self.state.search_space, conv=self.state.conversation
        )
        print("Update search space ######################\n", self.state.search_space)
        return

    @listen(get_axes_preferences)
    def hard_score_filter(self):
        self.state.skus = filter_explicit(self.state.skus, self.state.search_space)

    @listen(hard_score_filter)
    def soft_score_sort_decreasing(self):
        self.state.skus = get_sorted_skus_by_soft_score(self.state.skus, user_query=self.state.search_space)

    @listen(soft_score_sort_decreasing)
    def end_sorting_and_filtering(self):
        return

    @listen(get_axes_preferences)
    def start_justification_reasoning(self):
        reasonings = {}
        for field_name, value in self.state.search_space.model_dump().items():
            reasonings[field_name] = value["reasoning"]

        result = _justify(self.model, reasonings=reasonings)
        self.state.justification = result
        return self.state.justification

    @listen(or_(start_justification_reasoning, begin_preparing_empty_justification))
    def end_justification(self):
        return

    @listen(and_(ask_followup, end_justification))
    def prepare_response_and_justification(self):
        return

    @listen(and_(prepare_response_and_justification, end_sorting_and_filtering))
    def send_response(self):
        return {
            "justification": self.state.justification,
            "followup": self.state.followup,
            "search_space": self.state.search_space,
            "skus": self.state.skus,
        }
