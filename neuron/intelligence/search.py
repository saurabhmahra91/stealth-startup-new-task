from neuron.intelligence.justification import _justify
from neuron.intelligence.followup import _ask_followup
from neuron.intelligence.refinement import _refine_axes
from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel

from axes import Axes


def get_followup_axes():
    return Axes.model_json_schema()


class SearchState(BaseModel):
    query: str = ""
    search_space: Axes = Axes()


class Search(Flow[SearchState]):
    # model = "gpt-4o-mini"
    model = "ollama/gemma3:4b"

    @start()
    def receive_user_query(self):
        print(self.state)
        self.state.search_space = Axes()
        return self.state.query

    @listen(receive_user_query)
    def ask_followup(self, query):
        result = _ask_followup(model=self.model, query=query, search_space=self.state.search_space)
        print("The followup question asked = ", result)
        return result

    @listen(receive_user_query)
    async def refine_axes(self, query):
        self.state.search_space = await _refine_axes(query=query)
        print("Update search space ######################\n", self.state.search_space)
        return query

    @listen(refine_axes)
    def justify(self, query):
        result = _justify(self.model, search_space=self.state.search_space, query=query)
        return result


flow = Search()
flow.plot()
result = flow.kickoff(inputs={"query": "Hi"})
