import asyncio
import json
import logging

from litellm import completion

from .axes import AXIS_REGISTRY, Axes
from .refine_context import AxisRefinementContext
from .utils import extract_json_from_response

logger = logging.getLogger(__name__)


def AXIS_SYSTEM_PROMPT(axis_name):
    return (
        "You are an expert fashion shopping assistant. "
        f"You specialize in analyzing just one axis of a structured product search space at a time — in this case: `{axis_name}`. "
        "You use fashion expertise and logical reasoning to infer or update values for this axis only, without affecting the others. "
        "The input may be vibe-loaded or vague, but you're here to keep this fashion product search axis tight. "
        "To complete the task, you already have prepared the understanding of the user intent. "
    )


def AXIS_USER_PROMPT(intent, current_value, axis_name, axis_model_schema):
    return (
        "This the user intent that you have already figured out:\n "
        f"#################{intent}#################\n"
        "You have to intelligently update this pydantic model *in-place*, "
        "preserving existing information from prior queries unless the new input clarifies or overrides it. "
        f"This is the current search space for `{axis_name}` axis:\n"
        f"{current_value}\n"
        f"Your job is to refine the `{axis_name}` in the structured product search space.\n"
        f"- Focus *only* on updating `{axis_name}` based on the new query.\n"
        "- Preserve existing values unless there is a strong signal to change it.\n"
        "Respond in a valid JSON format that validates against the below JSON schema:\n"
        "#################\n"
        f"{axis_model_schema}\n"
        "#################\n"
        "Do not return natural language text. "
        "Do not include markdown tags like ```json. "
        'Do not include schema keys like "title", "type", or "properties". '
        "Only return the valid JSON for the updated axis. "
    )


def _build_axis_prompt(context: AxisRefinementContext, axis_name: str):
    system_prompt = {"role": "system", "content": AXIS_SYSTEM_PROMPT(axis_name=axis_name)}
    user_prompt = {
        "role": "user",
        "content": AXIS_USER_PROMPT(
            intent=context.intent_summary,
            current_value=json.dumps(axis_value_by_name(context.search_space, axis_name), indent=2),
            axis_name=axis_name,
            axis_model_schema=json.dumps(axis_model_by_name(axis_name).model_json_schema(), indent=2),
        ),
    }
    return [system_prompt, user_prompt]


def _parse_axis_response(response, axis_name):
    try:
        content = response["choices"][0]["message"]["content"]
        data = extract_json_from_response(content)
        return axis_model_by_name(axis_name)(**data)
    except Exception as e:
        logger.error(f"Error while refining the {axis_name} axis. LLM Output:\n{content}")
        logger.error(f"Exception: {str(e)}")
        return axis_model_by_name(axis_name)()


_AXIS_MODEL_MAP = dict(AXIS_REGISTRY)


def axis_model_by_name(name: str):
    try:
        return _AXIS_MODEL_MAP[name]
    except KeyError as e:
        raise ValueError(f"Axis model not found in AXIS_REGISTRY for: {name}") from e


def axis_value_by_name(search_space: Axes, name: str) -> dict:
    try:
        return search_space.model_dump()[name]
    except AttributeError as e:
        raise ValueError(f"Axis value not found in search space for: {name}") from e


async def _refine_single_axis(context: AxisRefinementContext, axis_name):
    messages = _build_axis_prompt(context, axis_name)
    response = completion(model=context.model, messages=messages)
    return _parse_axis_response(response, axis_name)


async def _refine_axis(context: AxisRefinementContext, axis_name):
    return (axis_name, await _refine_single_axis(context, axis_name))


async def _refine_axes(context: AxisRefinementContext) -> Axes:
    coroutines = [_refine_axis(context, name) for name in _AXIS_MODEL_MAP]
    results = await asyncio.gather(*coroutines)

    axis_instances = {name: result for name, result in results}
    logger.debug("Axis instances:\n%s", axis_instances)

    updated_search_space = Axes(**axis_instances)
    logger.debug("Updated search space:\n%s", updated_search_space)

    return updated_search_space
