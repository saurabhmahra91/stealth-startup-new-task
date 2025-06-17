import asyncio
import json
import logging

from litellm import completion

from .axes import AXIS_REGISTRY, Axes
from .utils import extract_json_from_response, format_chat_prompt, get_last_user_content

logger = logging.getLogger(__file__)


def AXIS_SYSTEM_PROMPT(axis_name):
    return f"""
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


def _build_axis_prompt(model, conv, axis_name, current_axis_value, axis_model):
    system_prompt = {"role": "system", "content": AXIS_SYSTEM_PROMPT(axis_name=axis_name)}
    user_prompt = {
        "role": "user",
        "content": AXIS_USER_PROMPT(
            query=get_last_user_content(conv),
            conv=format_chat_prompt(conv),
            axis_name=axis_name,
            current_value=json.dumps(current_axis_value, indent=2),
            axis_model_schema=json.dumps(axis_model.model_json_schema(), indent=2),
        ),
    }
    return [system_prompt, user_prompt]


def _parse_axis_response(response, axis_name, axis_model):
    try:
        content = response["choices"][0]["message"]["content"]
        data = extract_json_from_response(content)
        return axis_model(**data)
    except Exception as e:
        logger.error(f"Error while refining the {axis_name} axis. LLM Output:\n{content}")
        logger.error(f"Exception: {str(e)}")
        return axis_model()


async def _refine_single_axis(model, current_axis_value, conv, axis_name, axis_model):
    messages = _build_axis_prompt(model, conv, axis_name, current_axis_value, axis_model)
    response = completion(model=model, messages=messages)
    return _parse_axis_response(response, axis_name, axis_model)


async def _refine_axes(model, search_space: Axes, conv) -> Axes:
    async def refine_axis(axis_name, axis_model):
        current_value = search_space.model_dump()[axis_name]
        return axis_name, await _refine_single_axis(model, current_value, conv, axis_name, axis_model)

    coroutines = [refine_axis(name, mdl) for name, mdl in AXIS_REGISTRY]
    results = await asyncio.gather(*coroutines)

    axis_instances = {name: result for name, result in results}
    logger.debug("Axis instances:\n%s", axis_instances)

    updated_search_space = Axes(**axis_instances)
    logger.debug("Updated search space:\n%s", updated_search_space)

    return updated_search_space
