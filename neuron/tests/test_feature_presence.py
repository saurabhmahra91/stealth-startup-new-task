import unittest

from neuron.search.implicit.feature_presence import (
    get_attribute_flags,
    get_sorted_skus_by_soft_score,
    score_sku_against_query,
)


class TestSkuScoring(unittest.TestCase):
    def setUp(self):
        self.sku_with_full_match = {
            "occasion": "Party",
            "fit": "Regular",
            "fabric": "Cotton",
            "sleeve_length": "Short",
            "neckline": "V-neck",
            "length": "Midi",
            "pant_type": "Palazzo",
        }

        self.sku_with_partial_match = {
            "occasion": "Party",
            "fit": "Slim",
            "fabric": "",  # missing
            "sleeve_length": "Long",
            "neckline": "",
            "length": "Mini",
            "pant_type": "",
        }

        self.sku_with_no_match = {
            "occasion": "Work",
            "fit": "Slim",
            "fabric": "",  # missing
            "sleeve_length": "Long",
            "neckline": "",
            "length": "Mini",
            "pant_type": "",
        }

        self.user_query = {
            "occasion": ["party", "casual"],
            "fit": ["regular"],
            "fabric": ["cotton", "linen"],
            "neckline": ["v-neck"],
        }

    def test_get_attribute_flags_full(self):
        flags = get_attribute_flags(self.sku_with_full_match)
        self.assertTrue(all(flags.values()))

    def test_get_attribute_flags_partial(self):
        flags = get_attribute_flags(self.sku_with_partial_match)
        self.assertEqual(flags["fabric"], False)
        self.assertEqual(flags["neckline"], False)
        self.assertEqual(flags["pant_type"], False)
        self.assertEqual(flags["fit"], True)

    def test_score_sku_against_query_full(self):
        score = score_sku_against_query(self.sku_with_full_match, self.user_query)
        self.assertAlmostEqual(score, 1.0)  # all matched

    def test_score_sku_against_query_partial(self):
        score = score_sku_against_query(self.sku_with_partial_match, self.user_query)
        self.assertAlmostEqual(score, 0.5)

    def test_score_sku_against_no_match(self):
        score = score_sku_against_query(self.sku_with_no_match, self.user_query)
        self.assertAlmostEqual(score, 0.0)

    def test_get_sorted_skus_by_soft_score(self):
        skus = [self.sku_with_partial_match, self.sku_with_full_match]
        sorted_skus = get_sorted_skus_by_soft_score(skus, self.user_query)
        self.assertEqual(sorted_skus[0], self.sku_with_full_match)
        self.assertEqual(sorted_skus[1], self.sku_with_partial_match)


if __name__ == "__main__":
    unittest.main()
