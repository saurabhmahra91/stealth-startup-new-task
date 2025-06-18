import json
from litellm import completion
from .axes import Axes
from .utils import get_last_user_content, format_chat_prompt


def INTENT_GEN_SYSTEM_PROMPT(axes_schema):
    return (
        "You are a senior fashion strategist and stylist AI. "
        "Your job is to interpret a user's fashion intent by analyzing their queries and past interactions. "
        "You think holistically about the user's preferences, context, and changes in direction. "
        "You generate a structured reasoning summary that can guide multiple downstream product search axes. See some information of the axes below:\n"
        f"{axes_schema}\n"
        "You're not selecting products — you're forming a coherent *style intent profile* for the current session. "
        "Use cultural fashion norms, seasonality, occasion types, and implicit cues to reason smartly. "
        "Avoid contradictions, be concise, and prioritize relevance. "
    )

# "In the beginning, it might be possible that the search space is too broad or too narrow — this is because it's set to default in the start. "
# "The history is for your reference, it could be possible that the user changed their mind and started searching something very different. "


def INTENT_GEN_USER_PROMPT(conv, search_space: Axes):
    return (
        "The user is currently shopping for fashion items. Here's their latest message: "
        "#################\n"
        f"{get_last_user_content(conv)}\n"
        "#################\n "
        "Here is the full conversation history, from first message to latest: "
        "#################\n"
        f"{format_chat_prompt(conv)}\n"
        "#################\n "
        "This is the current product search space state:\n"
        "#################\n "
        f"{search_space.model_dump_json()}\n"
        "#################\n"
        "Generate a structured reasoning summary that explains how product search axes should be transformed in order to accomodate: \n"
        "1. The inferred overall user intent and mood (occasion, season, style direction, etc.). "
        "2. Any major updates in the user's thinking (e.g., changed occasion, added constraints). "
        "3. Budget-related implications, if mentioned. "
        "4. Vibes or aesthetic cues (casual, classy, streetwear, playful, etc.). "
        "5. Any specific attributes that now need to be emphasized or deprioritized.\n"
        "Output your response as a clean markdown without any extra commentary. "
        "Keep it factual and neutral in tone. "
    )


def _get_user_intent(model, conv, search_space):

    response = completion(
        model=model,
        messages=[
            {"role": "system", "content": INTENT_GEN_SYSTEM_PROMPT(axes_schema=Axes.model_json_schema())},
            {
                "role": "user",
                "content": INTENT_GEN_USER_PROMPT(conv, search_space),
            },
        ],
    )
    result = response["choices"][0]["message"]["content"]
    print("################\nUser intent interpretation == ", result)
    return result
