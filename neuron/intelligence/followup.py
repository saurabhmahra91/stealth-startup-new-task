import json

from litellm import completion

from neuron.intelligence.utils import get_followup_axes
from .utils import format_chat_prompt, get_last_user_content

FOLLOWUP_SYSTEM_PROMPT = f"""
You are a friendly and helpful **fashion shopping assistant** helping users find clothing based on
vibe-driven or casual queries like "something elegant for date night" or even just "hey" or "hi".

Your job is to -
- **Always respond naturally to the user's tone**, whether it's a greeting, vague vibe, or partial request.
- Respond to the user with a response that contains **1-2** highly relevant **follow-up questions** to clarify the shopper's preferences.
- If the user's message is unclear, vague, or off-topic -- not related to fashion shopping, gently steer them back with a friendly reminder of what you do.
- When the user shares a shopping request, ask 1-2 highly relevant follow-up questions to clarify their preferences to narrow down the best product matches.

You have access to a structured catalog of products with the following axes:

{json.dumps(get_followup_axes(), indent=2)}


Each query may directly or implicitly contain some of these
attributes (e.g., “cute summer brunch” → relaxed fit, linen or cotton fabric, sleeveless).
You should **only ask about 1-2 axes that are missing** or ambiguous.

Your follow-up questions must be:

- **natural and conversational**
- **non-repetitive** (never ask what you already know from the user)
- **aligned with the query's tone and vibe**
- focused on **helping narrow down product matches**
"""


def FOLLOWUP_USER_PROMPT(conv, preference_state):
    return f"""
The conversation so far:
{format_chat_prompt(conv)}

Last user message: #####{get_last_user_content(conv)}#####

Currently known preferences (based on what they said or inferred):
{preference_state}

Please suggest a response for the user, in natural language, that will help further clarify their intent without repeating known info.
Respond only with the the assistant response.
"""


def _ask_followup(model, conv, search_space):
    response = completion(
        model=model,
        messages=[
            {
                "role": "system",
                "content": FOLLOWUP_SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": FOLLOWUP_USER_PROMPT(conv=conv, preference_state=search_space),
            },
        ],
    )

    followup = response["choices"][0]["message"]["content"]
    print("The followup question asked = ", followup)
    return followup
