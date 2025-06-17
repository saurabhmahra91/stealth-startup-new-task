import asyncio
import json
from collections.abc import Coroutine

from .axes import AXIS_REGISTRY, Axes
from .crews.refiner import search_axis_refiner
from .utils import (extract_json_from_response, format_chat_prompt,
                    get_last_user_content)


async def _refined_axis(current_axis_value, conv, axis_name, axis_model):
    result = await search_axis_refiner.kickoff_async(
        inputs={
            "conv": format_chat_prompt(conv),
            "query": get_last_user_content(conv),
            "axis_name": axis_name,
            "current_value": json.dumps(current_axis_value, indent=2),
            "axis_model": json.dumps(axis_model.model_json_schema(), indent=2),
            "axis_model_schema": json.dumps(axis_model.model_json_schema(), indent=2),
        }
    )
    try:
        model_instance = axis_model(**extract_json_from_response(result.raw))
    except Exception:
        print(f"this was the result for the model {axis_model}\n#####################\n", result.raw)
        raise
    return model_instance


async def _refine_axes(search_space: Axes, conv) -> Axes:
    result_coroutines = []

    for axis_name, axis_model in AXIS_REGISTRY:
        result_coro: Coroutine = _refined_axis(search_space.model_dump()[axis_name], conv, axis_name, axis_model)
        result_coroutines.append(result_coro)

    results = await asyncio.gather(*result_coroutines)
    axis_instances = dict(
        (axis_name, result) for (axis_name, axis_model), result in zip(AXIS_REGISTRY, results, strict=True)
    )
    print("axis instances ************************************************\n", axis_instances)
    updated_search_space = Axes(**axis_instances)
    print("Update search space ######################\n", updated_search_space)
    return updated_search_space
