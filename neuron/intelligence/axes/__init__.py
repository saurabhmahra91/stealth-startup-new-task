from .enum_axes import (
    Category,
    Occasion,
    Sizes,
    Fabric,
    Fit,
    SleeveLength,
    Neckline,
    Length,
    PantType,
)
from pydantic import BaseModel
from .price_axis import Price

AXIS_REGISTRY: tuple[tuple[str, BaseModel]] = (
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
