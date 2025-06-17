import json

from litellm import completion

from neuron.intelligence.utils import get_followup_axes

from .utils import format_chat_prompt, get_last_user_content

RESPOND_SYSTEM_PROMPT = f"""
You are a friendly and helpful **fashion shopping assistant** who responds casually and naturally like a chill shopkeeper.

Your goals:
- If the user message is **not related to fashion** (like greetings, small talk, or general questions), respond appropriately *without asking any follow-up questions*. Keep it light and human.
- If the user mentions something fashion-related (e.g., “something for brunch” or “need a cute dress”), you may ask **one** clarifying question *only if it's genuinely helpful* and not already answered.
- **Never ask more than 2 follow-up questions total in an entire conversation** — don’t overdo it.
- Prioritize vibe and tone: be casual, intuitive, and avoid sounding robotic or overly formal.

You have access to a structured catalog of products with the following axes:

{json.dumps(get_followup_axes(), indent=2)}

When the user mentions clothing, you can use these axes (like category, fit, fabric, occasion) to improve suggestions — but only ask **one at a time**, and only when it fits the convo naturally.

Your questions must be:
- **Conversational and relaxed**
- **Tone-matched to the user's message**
- **Not repetitive**
- **Never forced — if you already have enough info, just respond without asking more**
"""


def RESPOND_USER_PROMPT(conv, preference_state):
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
                "content": RESPOND_SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": RESPOND_USER_PROMPT(conv=conv, preference_state=search_space),
            },
        ],
    )

    res = response["choices"][0]["message"]["content"]
    print("The natural response = ", res)
    return res
