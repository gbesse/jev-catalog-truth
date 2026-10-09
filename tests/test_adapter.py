import unittest

from app import adapt, load_example
from review_core import InputError


class AdapterTests(unittest.TestCase):
    def test_owner_and_lifecycle_change_are_reviewed(self):
        parsed = adapt(load_example())
        self.assertEqual(parsed["subject"], "checkout-api")
        self.assertIn("owner_changed", parsed["flags"])
        self.assertIn("lifecycle_changed", parsed["flags"])

    def test_invalid_yaml_and_different_name_rejected(self):
        case = load_example()
        case["after_yaml"] = "!!python/object/apply:os.system ['false']"
        with self.assertRaises(InputError):
            adapt(case)
        case = load_example()
        case["after_yaml"] = case["after_yaml"].replace("checkout-api", "other-api")
        with self.assertRaises(InputError):
            adapt(case)


if __name__ == "__main__":
    unittest.main()
