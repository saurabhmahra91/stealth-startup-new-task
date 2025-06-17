from crewai.flow.flow import Flow, and_, listen, start
from pydantic import BaseModel

from neuron.intelligence.followup import _ask_followup
from neuron.intelligence.justification import _justify
from neuron.intelligence.refinement import _refine_axes

from .axes import Axes


def get_followup_axes():
    return Axes.model_json_schema()


class SearchState(BaseModel):
    conversation: list[dict] = []
    search_space: Axes = Axes()
    justification: str = ""
    followup: str = ""


class SearchFlow(Flow[SearchState]):
    # model = "gpt-4o-mini"
    model = "ollama/gemma3:4b"

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

    @listen(receive_user_query)
    async def refine_axes(self, conv):
        self.state.search_space = await _refine_axes(conv=conv)
        print("Update search space ######################\n", self.state.search_space)
        return conv

    @listen(refine_axes)
    def justify(self, conv):
        result = _justify(self.model, search_space=self.state.search_space, conv=conv)
        self.state.justification = result
        return result

    @listen(and_(ask_followup, refine_axes, justify))
    def send_response(self):
        return {
            "justification": self.state.justification,
            "followup": self.state.followup,
            "search_space": self.state.search_space,
        }
