from litellm import completion
import asyncio
import json
from collections.abc import Coroutine

from .axes import AXIS_REGISTRY, Axes
from .crews.refiner import search_axis_refiner
from .utils import extract_json_from_response, format_chat_prompt, get_last_user_content


AXIS_SYSTEM_PROMPT = """
You are an expert fashion shopping assistant. You specialize in analyzing just one axis of a structured product search space at a time — in this case: `{axis_name}`.
You use fashion expertise and logical reasoning to infer or update values for this axis only, without affecting the others.
The input may be vibe-loaded or vague, but you're here to keep this fashion product search axis tight.
"""


def AXIS_USER_PROMPT(query, conv, current_value, axis_name, axis_model_schema):
    return f"""
The user's current message is:
#################
{query}
#################

For context, this is the full conversation history:
#################
{conv}
#################

You have to intelligently update this pydantic model *in-place*, preserving existing information from prior queries unless the new input clarifies or overrides it.
This is the current search space for `{axis_name}` axis:
{current_value}

In the beginning, it might be possible that the search space is too broad or too narrow — this is because it's set to default in the start.

The history is for your reference, it could be possible that the user changed their mind and started searching something very different.

Your job is to refine the `{axis_name}` in the structured product search space.

- Focus *only* on updating `{axis_name}` based on the new query.
- Preserve existing values unless there is a strong signal to change it.

Respond in a valid JSON format that validates against the below JSON schema:
#################
{axis_model_schema}
#################

Do not return natural language text.
Do not include markdown tags like ```json.
Do not include schema keys like "title", "type", or "properties".
Only return the valid JSON for the updated axis.
"""


async def _refined_axis(model, current_axis_value, conv, axis_name, axis_model):
    response = completion(
        model=model,
        messages=[
            {"role": "system", "content": AXIS_SYSTEM_PROMPT.format(axis_name=axis_name)},
            {
                "role": "user",
                "content": AXIS_USER_PROMPT(
                    query=get_last_user_content(conv),
                    conv=format_chat_prompt(conv),
                    axis_name=axis_name,
                    current_value=json.dumps(current_axis_value, indent=2),
                    axis_model_schema=json.dumps(axis_model.model_json_schema(), indent=2),
                ),
            },
        ],
    )

    try:
        model_instance = axis_model(**extract_json_from_response(response["choices"][0]["message"]["content"]))
    except Exception:
        print(f"Axis: {axis_name} | Raw LLM Output:\n{response['choices'][0]['message']['content']}")
        raise

    return model_instance


async def _refine_axes(model, search_space: Axes, conv) -> Axes:
    result_coroutines = []

    for axis_name, axis_model in AXIS_REGISTRY:
        result_coro: Coroutine = _refined_axis(model, search_space.model_dump()[axis_name], conv, axis_name, axis_model)
        result_coroutines.append(result_coro)

    results = await asyncio.gather(*result_coroutines)
    axis_instances = dict(
        (axis_name, result) for (axis_name, axis_model), result in zip(AXIS_REGISTRY, results, strict=True)
    )
    print("axis instances ************************************************\n", axis_instances)
    updated_search_space = Axes(**axis_instances)
    print("Update search space ######################\n", updated_search_space)
    return updated_search_space
