# from neuron.intelligence.axes import example_axes
# from neuron.search.explicit import filter_explicit

# filter_explicit(example_axes)

from neuron.intelligence.flow import SearchFlow
from neuron.intelligence.utils import get_last_user_content

flow = SearchFlow()
messages = [{"role": "user", "content": "Hi"}]
print(get_last_user_content(messages))
a = flow.kickoff({"conversation": messages})
print(a)
