
import unittest
from unittest.mock import patch
from feature2_contributor_expertise import run_feature_2

class TestFeature2Extra(unittest.TestCase):
    @patch('feature2_contributor_expertise.DataLoader')
    def test_run_feature2_no_matching_label(self, MockDataLoader):
        # Provide issues without the target label
        MockDataLoader().get_issues.return_value = []
        with patch('builtins.input', return_value='nonexistent'):
            try:
                run_feature_2()
            except Exception as e:
                self.fail(f"run_feature_2 crashed on no matching label: {e}")

if __name__ == '__main__':
    unittest.main()
