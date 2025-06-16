from pydantic import BaseModel, Field
from typing import Literal


class Category(BaseModel):
    values: list[Literal["top", "dress", "skirt", "pants"]] = []
    reasoning: str = Field(
        description="The reasoning of why did you come up with the values you came with, given the user query.",
        default="",
    )


class Occasion(BaseModel):
    values: list[Literal["party", "vacation", "everyday", "work", "evening"]] = []
    reasoning: str = Field(
        description="The reasoning of why did you come up with the values you came with, given the user query.",
        default="",
    )


class Sizes(BaseModel):
    values: list[Literal["xs", "s", "m", "l", "xl"]] = []
    reasoning: str = Field(
        description="The reasoning of why did you come up with the values you came with, given the user query.",
        default="",
    )


class Fit(BaseModel):
    values: list[
        Literal[
            "relaxed",
            "body hugging",
            "stretch to fit",
            "tailored",
            "flowy",
            "slim",
            "sleek and straight",
            "oversized",
        ]
    ] = []
    reasoning: str = Field(
        description="The reasoning of why did you come up with the values you came with, given the user query.",
        default="",
    )


class Fabric(BaseModel):
    values: list[
        Literal[
            "linen",
            "cotton",
            "rayon",
            "satin",
            "silk",
            "tencel",
            "crepe",
            "velvet",
            "denim",
            "wool-blend",
            "polyester",
            "chiffon",
            "jersey",
            "tweed",
            "lace",
            "scuba knit",
            "modal jersey",
            "lamé",
            "organza",
            "ribbed jersey",
            "tulle",
            "vegan leather",
        ]
    ] = []
    reasoning: str = Field(
        description="The reasoning of why did you come up with the values you came with, given the user query.",
        default="",
    )


class SleeveLength(BaseModel):
    values: list[
        Literal[
            "sleeveless",
            "short sleeves",
            "quarter sleeves",
            "full sleeves",
            "long sleeves",
            "straps",
            "tube",
            "balloon sleeves",
            "cap sleeves",
            "bishop sleeves",
            "cropped long sleeves",
            "short flutter sleeves",
            "mockneck",
            "one-shoulder",
            "puff sleeves",
        ]
    ] = []
    reasoning: str = Field(
        description="The reasoning of why did you come up with the values you came with, given the user query.",
        default="",
    )


class Neckline(BaseModel):
    values: list[
        Literal[
            "sweetheart",
            "square neck",
            "v neck",
            "boat neck",
            "tubetop",
            "halter",
            "collar",
            "cowl neck",
            "polo collar",
            "illusion bateau",
            "round neck",
            "one-shoulder",
        ]
    ] = []
    reasoning: str = Field(
        description="The reasoning of why did you come up with the values you came with, given the user query.",
        default="",
    )


class Length(BaseModel):
    values: list[
        Literal[
            "mini",
            "short",
            "midi",
            "maxi",
            "ankle length",
            "wide-legged",
            "wide hem",
            "low-rise",
            "mid-rise",
            "straight ankle",
            "flared",
        ]
    ] = []
    reasoning: str = Field(
        description="The reasoning of why did you come up with the values you came with, given the user query.",
        default="",
    )


class PantType(BaseModel):
    values: list[
        Literal[
            "wide-legged",
            "straight ankle",
            "flared",
            "wide hem",
            "low-rise",
            "mid-rise",
            "ankle length",
            "slim",
        ]
    ] = []
    reasoning: str = Field(
        description="The reasoning of why did you come up with the values you came with, given the user query.",
        default="",
    )
