from pydantic import BaseModel, Field


class Price(BaseModel):
    max_usd: float = 100.0
    min_usd: float = 0.0
    reasoning: str = Field(
        description=(
            "The reasoning of why did you come up with the values of max_usd and min_usd, given "
            "the user query. Note that all the products are between 0 than 100$."
        ),
        default="",
    )


import json

print(json.dumps(Price.model_json_schema()))
