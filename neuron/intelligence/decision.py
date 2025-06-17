from litellm import completion

from .utils import format_chat_prompt, get_last_user_content

QUERY_ROUTER_SYSTEM_PROMPT = """You are a query router for a fashion e-commerce AI search system.
Your job is to determine if a user's query should be processed by the AI fashion search
engine or handled through a different route.

IMPORTANT: You must respond with ONLY a JSON object containing your decision and reasoning.

The AI fashion search system is designed to help users find clothing and fashion items based on:
- Product categories (tops, dresses, skirts, pants)
- Occasions (party, vacation, everyday, work, evening)
- Sizes, colors, fits, fabrics
- Price ranges
- Style preferences
- Fashion advice and recommendations

ROUTE TO AI SEARCH if the query is:
- Looking for specific clothing items or fashion products
- Asking for fashion recommendations or advice
- Describing an occasion and needing outfit suggestions
- Asking about style, fit, or fashion trends
- Requesting help with wardrobe or clothing choices
- Expressing preferences for clothing attributes (color, size, price, etc.)
- Following up on previous fashion-related queries

DO NOT ROUTE TO AI SEARCH if the query is:
- General greetings without fashion context ("Hi", "Hello", "How are you?")
- Questions related to fashion but without the intension to search fashion products in the website.
- Requests for non-fashion information or services
- Spam, inappropriate content, or nonsensical input

Response format: Just one character, either 0 (should not search) or 1 (should search)


Examples of your responses:

For "I need a dress for a wedding":
Response: 1

For "Hi there":
0

For "What's the weather like?":
0

Something cute for brunch:
1
"""


def QUERY_ROUTER_USER_PROMPT(conv) -> str:
    """
    Generate user prompt for query routing decision

    Args:
        user_query: The current user query to route
        conversation_context: Optional previous conversation for context
    """

    return f"""
History of conversation:
{format_chat_prompt(conv)}

Current user query: {get_last_user_content(conv)}

Determine if this query should be routed to the AI fashion search system. Consider:
1. Is this related to finding, recommending discussing fashion/clothing items?
2. Does the user need help with fashion choices or style decisions?
3. Is this a continuation of a fashion-related conversation?

Respond with 0 or 1 integer only."""


def route_query(model, conv) -> bool:
    response = completion(
        model=model,
        messages=[
            {"role": "system", "content": QUERY_ROUTER_SYSTEM_PROMPT},
            {"role": "user", "content": QUERY_ROUTER_USER_PROMPT(conv)},
        ],
    )

    result_text = response["choices"][0]["message"]["content"]

    return not (result_text.find("0") != -1 and result_text.find("1") == -1)
