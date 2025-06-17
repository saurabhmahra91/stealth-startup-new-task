from litellm import completion

from .utils import format_chat_prompt, get_last_user_content

JUSTIFICATION_SYSTEM_PROMPT = """
You are a fashion assistant who helped a user discover clothing that fits their style and preferences.
You have already selected search space values (like category, fabric, occasion, etc.) based on the user's query.

Each attribute includes a "reasoning" field explaining *exactly why* it was selected.

Your task is to generate a short, friendly 2-3 line justification combining all of these individual reasonings.
You must use only the information provided in the reasoning fields.
Do not assume or invent additional motivations such as comfort or trendiness unless explicitly stated.
"""


def JUSTIFICATION_USER_PROMPT(reasonings):
    return f"""
Here is the reasoning for different axes for a fashion search query:
{reasonings}

Please generate a positive natural-sounding explanation (2-3 lines) summarizing this reasoning.
Ensure the response starts directly with the
justification. No framing or commentary.
"""


def _justify(model, reasonings):
    response = completion(
        model=model,
        messages=[
            {"role": "system", "content": JUSTIFICATION_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": JUSTIFICATION_USER_PROMPT(reasonings),
            },
        ],
    )
    result = response["choices"][0]["message"]["content"]
    print("################\nJustification == ", result)
    return result
