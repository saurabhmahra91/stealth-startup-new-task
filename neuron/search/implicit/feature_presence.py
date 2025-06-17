from ...intelligence.axes import Axes

PRESENCE_FLAGS = ["occasion", "fit", "fabric", "sleeve_length", "neckline", "length", "pant_type"]


def get_attribute_flags(sku: dict[str, str]) -> dict[str, bool]:
    """
    Returns a dict of flags indicating which attribute values are present in a SKU record.
    Useful for soft scoring.
    """
    return {key: bool(sku.get(key, "").strip()) for key in PRESENCE_FLAGS}


def score_sku_against_query(sku: dict[str, str], user_query: Axes) -> float:
    """
    Score a single SKU against a structured user query using soft matching.
    """

    flags = get_attribute_flags(sku)
    score = 0
    max_score = 0

    for attr in PRESENCE_FLAGS:
        preferred_values = getattr(user_query, attr).values
        attr_key = attr.lower()
        has_attr = flags.get(attr_key, False)

        if has_attr:
            sku_value = sku.get(attr_key, "").lower()
            max_score += 1
            if any(val.lower() in sku_value for val in preferred_values):
                score += 1

    return score / max_score if max_score else 0.0


def get_sorted_skus_by_soft_score(skus: list[dict[str, str]], user_query: Axes) -> list[dict[str, str]]:
    """
    Given a list of SKUs (dicts) and a user query, return SKUs sorted by soft match score (desc).
    """
    scores = [score_sku_against_query(sku, user_query) for sku in skus]

    scored_skus = [(sku, score) for sku, score in zip(skus, scores, strict=True)]

    sorted_skus = sorted(scored_skus, key=lambda x: x[1], reverse=True)

    return [sku for sku, _ in sorted_skus]
