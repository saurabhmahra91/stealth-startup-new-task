import litellm
from crewai import LLM, Crew, Process

from ..agents.search_space_updater import search_space_axis_agent
from ..tasks.update_search_space import refine_axis_task

litellm._turn_on_debug()
litellm.disable_end_user_cost_tracking = True
litellm.disable_spend_logs = True
litellm.disable_spend_updates = True


ollama_llm = LLM(model="ollama/gemma3:4b", base_url="http://localhost:11434", api_key="")

search_axis_refiner = Crew(
    agents=[search_space_axis_agent],
    tasks=[refine_axis_task],
    verbose=True,
    process=Process.sequential,
    chat_llm=ollama_llm,
    manager_llm=ollama_llm,
    planning_llm=ollama_llm,
)
