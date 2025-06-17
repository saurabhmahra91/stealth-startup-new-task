import os

from crewai.flow import router
from crewai.flow.flow import Flow, and_, listen, or_, start
from pydantic import BaseModel

from .axes import Axes
from .decision import route_query
from .followup import _ask_followup
from .justification import _justify
from .refinement import _refine_axes


def get_followup_axes():
    return Axes.model_json_schema()


class SearchState(BaseModel):
    conversation: list[dict] = []
    search_space: Axes = Axes()
    justification: str = ""
    followup: str = ""


class SearchFlow(Flow[SearchState]):
    model = os.environ.get("MODEL", "ollama/gemma3:4b")

    @start()
    def receive_user_query(self):
        print(self.state.conversation)
        self.state.search_space = Axes()
        return self.state.conversation

    @listen(receive_user_query)
    def ask_followup(self, conv):
        result = _ask_followup(model=self.model, conv=conv, search_space=self.state.search_space)
        self.state.followup = result
        print("The followup question asked = ", result)
        return result

    @router(receive_user_query)
    def should_refine_search(self, conv):
        should_refine = route_query(self.model, conv)
        if should_refine:
            return "SHOULD_REFINE_SEARCH"
        else:
            return "SHOULD_NOT_REFINE_SEARCH"

    @listen("SHOULD_REFINE_SEARCH")
    async def refine_axes(self, conv):
        self.state.search_space = await _refine_axes(conv=conv)
        print("Update search space ######################\n", self.state.search_space)
        return conv

    @listen(refine_axes)
    def justify(self, conv):
        result = _justify(self.model, search_space=self.state.search_space, conv=conv)
        self.state.justification = result
        return self.state.justification

    @listen("SHOULD_NOT_REFINE_SEARCH")
    def send_empty_justification(self):
        self.state.justification = ""
        return self.state.justification

    @listen(or_(and_(ask_followup, justify), and_(ask_followup, send_empty_justification)))
    def send_response(self):
        return {
            "justification": self.state.justification,
            "followup": self.state.followup,
            "search_space": self.state.search_space,
        }
