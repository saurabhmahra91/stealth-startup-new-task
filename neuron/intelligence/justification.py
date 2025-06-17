from litellm import completion

from .utils import format_chat_prompt, get_last_user_content

JUSTIFICATION_SYSTEM_PROMPT = """
You are a fashion assistant who helped a user discover clothing that fits their style and preferences.
You are always able to justify *why* a certain category, size, fabric,
or other attribute is part of the current search space that you have decided.

You are given a Pydantic model instance containing:
- `values`: the current values of the search space for a multiple attributes that you came up with
- `reasoning`: the logic or contextual justification for why those values were selected or preserved that you prepared.

Use this model instance to write a justification summary (not more than 2 lines) which you will give to the user,
clearly explaining *why* did you show the user the products (indirectly why did you prepared the current search space,
based on his query.
"""


def JUSTIFICATION_USER_PROMPT(instance, conv):
    return f"""
Here is the current state of the axes for a fashion search session:
{instance}

This was the user's last query: {get_last_user_content(conv)}

This is the conversation history with the user: {format_chat_prompt(conv)}

Please generate a positive natural-sounding explanation (2 lines) summarizing why did you chose these values of the
current search space, using the reasoning fields to explain the logic. Ensure the response starts directly with the
justification. No framing or commentary.
"""


def _justify(model, search_space, conv):
    response = completion(
        model=model,
        messages=[
            {"role": "system", "content": JUSTIFICATION_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": JUSTIFICATION_USER_PROMPT(search_space, conv),
            },
        ],
    )
    result = response["choices"][0]["message"]["content"]
    print("################\nJustification == ", result)
    return result
