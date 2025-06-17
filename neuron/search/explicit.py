from ..intelligence.axes import Axes, Category, Price, Sizes, example_axes
from .utils import load_fashion_data

explicit_fields = {"price", "category", "sizes"}


def filter_explicit(skus: list[dict], search_space: Axes):
    filtered = []

    min_price = search_space.price.min_usd
    max_price = search_space.price.max_usd
    allowed_sizes = set(search_space.sizes.values)
    allowed_cats = set(search_space.category.values)

    for row in skus:
        if not (min_price <= row["usd_price"] <= max_price):
            continue

        # Check sizes
        row_sizes = set(row["available_sizes"])
        if allowed_sizes and not row_sizes & allowed_sizes:
            continue

        # Check category
        row_cat = row.get("category", "")
        if allowed_cats and row_cat not in allowed_cats:
            continue

        filtered.append(row)

    return filtered
