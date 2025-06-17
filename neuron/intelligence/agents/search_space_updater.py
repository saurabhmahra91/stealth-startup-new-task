from crewai import Agent


system_template = """You are {role}
{backstory}
Your goal is: {goal}
"""

prompt_temlate = """Please complete this task --
Task: {input}"""


search_space_axis_agent = Agent(
    role="Expert shopping assistant.",
    goal="Update the '{axis_name}' axis field in a structured product search space "
    "based on the user's current query and previous context. "
    "Translate ambiguous fashion lingo into precise values for this axis only.",
    backstory=(
        "You specialize in analyzing just one axis of a structured search space at a time — in this case: `{axis_name}`\n"
        "You use fashion expertise and logical reasoning to infer or update values for this axis only, "
        "without affecting the others. The input may be vibe loaded, or vague, but you're here to keep this "
        "fashion product search axis tight."
    ),
    tools=[],
    system_template=system_template,
    prompt_template=prompt_temlate,
    verbose=True,
    allow_delegation=False,
    reasoning=False,
)
