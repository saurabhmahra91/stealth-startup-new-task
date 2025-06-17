import json
import re

from .axes import Axes


def extract_json_from_response(text: str) -> dict:
    """
    Extract and parse the JSON object from a string that may contain Markdown-style code fences.

    Args:
        text (str): The raw response text, possibly wrapped in ```json ... ```

    Returns:
        dict: The parsed JSON object.

    Raises:
        ValueError: If no valid JSON can be extracted or parsed.
    """

    # Try to find JSON code block
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)

    if not match:
        # Fallback: try to find the first JSON-looking object in text
        match = re.search(r"(\{.*?\})", text, re.DOTALL)

    if match:
        json_str = match.group(1)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Found JSON-like string but failed to parse: {e}") from e

    raise ValueError("No JSON object found in response.")


def get_followup_axes():
    return Axes.model_json_schema()


def get_last_user_content(conv: list[dict]):
    return next(msg["content"] for msg in reversed(conv) if msg["role"] == "user")


def format_chat_prompt(messages: list[dict]) -> str:
    prompt = []
    for msg in messages:
        role = msg["role"].capitalize()
        content = msg["content"].strip()
        content = content.split('</justification>')[-1].strip()
        prompt.append(f"{role}: {content}")
    return "\n".join(prompt)
