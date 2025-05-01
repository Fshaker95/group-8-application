import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from model import Issue
from feature3 import feature3

class TestFeature3(unittest.TestCase):

    @patch("feature3.plt.show")
    @patch("feature3.plt.boxplot")
    @patch("feature3.plt.hist")
    @patch("feature3.DataLoader")
    def test_feature3_with_valid_issues(self, MockLoader, mock_hist, mock_boxplot, mock_show):
        issue1 = MagicMock(spec=Issue)
        issue1.created_date = datetime(2023, 1, 1)
        issue1.closed_date = datetime(2023, 1, 5)
        issue1.url = "http://example.com/1"

        issue2 = MagicMock(spec=Issue)
        issue2.created_date = datetime(2023, 1, 10)
        issue2.closed_date = datetime(2023, 1, 15)
        issue2.url = "http://example.com/2"

        MockLoader.return_value.get_issues.return_value = [issue1, issue2]

        feature3()

        self.assertTrue(mock_hist.called)
        self.assertTrue(mock_boxplot.called)
        self.assertTrue(mock_show.called)

    @patch("feature3.plt.show")
    @patch("feature3.DataLoader")
    def test_feature3_no_issues(self, MockLoader, mock_show):
        MockLoader.return_value.get_issues.return_value = []
        feature3()
        self.assertFalse(mock_show.called)

    @patch("feature3.plt.show")
    @patch("feature3.DataLoader")
    def test_feature3_skips_issues_with_missing_dates(self, MockLoader, mock_show):
        issue1 = MagicMock(spec=Issue)
        issue1.created_date = None
        issue1.closed_date = datetime(2023, 1, 5)
        issue1.url = "http://example.com/3"

        issue2 = MagicMock(spec=Issue)
        issue2.created_date = datetime(2023, 1, 10)
        issue2.closed_date = None
        issue2.url = "http://example.com/4"

        MockLoader.return_value.get_issues.return_value = [issue1, issue2]

        feature3()
        self.assertFalse(mock_show.called)

    @patch("feature3.plt.show")
    @patch("feature3.DataLoader")
    def test_feature3_handles_zero_day_issues(self, MockLoader, mock_show):
        issue = MagicMock(spec=Issue)
        issue.created_date = datetime(2023, 1, 1)
        issue.closed_date = datetime(2023, 1, 1)
        issue.url = "http://example.com/5"

        MockLoader.return_value.get_issues.return_value = [issue]

        feature3()
        self.assertTrue(mock_show.called)

    @patch("feature3.plt.show")
    @patch("feature3.DataLoader")
    def test_feature3_handles_invalid_date_math(self, MockLoader, mock_show):
        issue = MagicMock(spec=Issue)
        issue.created_date = "bad-date"
        issue.closed_date = "bad-date"
        issue.url = "http://example.com/6"

        MockLoader.return_value.get_issues.return_value = [issue]

        feature3()
        self.assertFalse(mock_show.called)

if __name__ == "__main__":
    unittest.main()
