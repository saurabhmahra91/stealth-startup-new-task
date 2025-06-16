from crewai import Task
from agents.search_space_updater import search_space_axis_agent


refine_axis_task = Task(
    description=(
        "The user's current message is:\n"
        "#################\n"
        "{query}\n"
        "#################\n"
        "You have to intelligently update this pydantic model *in-place*, preserving existing information from"
        "prior queries unless the new input clarifies or overrides it."
        "Your job is to refine the `{axis_name}` in the structured product search space.\n"
        "- Focus *only* on updating `{axis_name}` based on the new query.\n"
        "- Preserve existing values unless there is a strong signal to change it.\n"
        "Your fashion intuition, logic, and memory of past context should help you interpret and refine this axis well."
    ),
    expected_output=(
        "Respond in a valid JSON format that when run validation against the below JSON schema would work.\n"
        "#################\n"
        "{axis_model_schema}\n"
        "#################\n"
        "Do not return natural language text. Your JSON response is supposed to validate when ran through the schema, "
        r"not mimic it!! Understand that keys such as \"properties\", \"title\", \"type\", etc. that are part of a JSON "
        "schema should never appear in "
        "the final response. Do not include markdown tags such as ```json in your response."
    ),
    agent=search_space_axis_agent,
    tools=[],
    # output_file="task_out_{axis_name}.json",
)
