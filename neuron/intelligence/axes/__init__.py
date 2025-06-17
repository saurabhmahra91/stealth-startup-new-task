from pydantic import BaseModel

from .enum_axes import (Category, Fabric, Fit, Length, Neckline, Occasion,
                        PantType, Sizes, SleeveLength)
from .price_axis import Price

AXIS_REGISTRY = (
    ("category", Category),
    ("occasion", Occasion),
    ("sizes", Sizes),
    ("fabric", Fabric),
    ("fit", Fit),
    ("sleeve_length", SleeveLength),
    ("neckline", Neckline),
    ("length", Length),
    ("pant_type", PantType),
    ("price", Price),
)


class Axes(BaseModel):
    category: Category = Category()
    occasion: Occasion = Occasion()
    sizes: Sizes = Sizes()
    fabric: Fabric = Fabric()
    fit: Fit = Fit()
    sleeve_length: SleeveLength = SleeveLength()
    neckline: Neckline = Neckline()
    length: Length = Length()
    pant_type: PantType = PantType()
    price: Price = Price()


example_axes = Axes(
    category=Category(
        values=["top", "dress"],
        reasoning="User mentioned both 'blouses' and 'summer dresses', which map to 'top' and 'dress'.",
    ),
    occasion=Occasion(
        values=["vacation", "party"],
        reasoning="The query suggested beach vibes and a festive tone, implying vacation and party.",
    ),
    sizes=Sizes(
        values=["s", "m", "l"], reasoning="Sizes 'S' to 'L' were inferred from average fit ranges for similar products."
    ),
    fabric=Fabric(
        values=["cotton", "linen"],
        reasoning="User emphasized breathable and natural fabrics, which matches cotton and linen.",
    ),
    fit=Fit(
        values=["relaxed", "flowy"], reasoning="The words 'comfortable' and 'breezy' suggest relaxed and flowy fits."
    ),
    sleeve_length=SleeveLength(
        values=["short sleeves", "sleeveless"],
        reasoning="Summer clothing typically avoids full sleeves; user also said 'no sleeves please'.",
    ),
    neckline=Neckline(
        values=["v neck", "halter"], reasoning="Mentions of casual and cool neckline styles suggest V-neck and halter."
    ),
    length=Length(
        values=["midi", "mini"],
        reasoning="The query indicated a preference for skirts above the ankle, hence midi and mini.",
    ),
    pant_type=PantType(
        values=["mid-rise", "flared"], reasoning="The phrase 'retro jeans' hints at flared and mid-rise cuts."
    ),
    price=Price(
        min_usd=0.0,
        max_usd=60.0,
        reasoning="User specified 'budget under $70' so we capped it at $60 to allow filtering margin.",
    ),
)
