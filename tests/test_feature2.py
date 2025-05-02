
import unittest
from unittest.mock import patch
from feature2_contributor_expertise import run_feature_2
from model import Issue, Event

class TestFeature2(unittest.TestCase):
    @patch('feature2_contributor_expertise.DataLoader')
    def test_run_feature2_with_mock_data(self, MockDataLoader):
        # Create mock issues
        issue1 = Issue()
        issue1.number = 1
        issue1.labels = ['bug']
        issue1.creator = 'alice'
        issue1.events = [Event({'event_type': 'commented', 'author': 'bob', 'event_date': '2024-01-01T12:00:00Z'})]

        issue2 = Issue()
        issue2.number = 2
        issue2.labels = ['bug']
        issue2.creator = 'alice'
        issue2.events = [Event({'event_type': 'commented', 'author': 'carol', 'event_date': '2024-01-02T12:00:00Z'})]

        # Patch DataLoader.get_issues to return our mock list
        MockDataLoader().get_issues.return_value = [issue1, issue2]

        # Patch input() to automatically return 'bug' as label input
        with patch('builtins.input', return_value='bug'):
            try:
                run_feature_2()
            except Exception as e:
                self.fail(f"run_feature_2 crashed with exception: {e}")

if __name__ == '__main__':
    unittest.main()
