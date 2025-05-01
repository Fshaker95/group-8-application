import unittest
from datetime import datetime
from unittest.mock import patch, MagicMock
from feature1_temporal_analysis import process_issues, run_feature_1

class TestProcessIssuesLogic(unittest.TestCase):
    def test_empty_input(self):
        months, counts, avgs = process_issues([])
        self.assertEqual(months, [])
        self.assertEqual(counts, [])
        self.assertEqual(avgs, [])

    def test_single_month_all_closed(self):
        class Dummy:
            def __init__(self, c, x):
                self.created_date = c
                self.closed_date = x

        issues = [
            Dummy(datetime(2020, 5, 1), datetime(2020, 5, 3)),
            Dummy(datetime(2020, 5, 10), datetime(2020, 5, 14))
        ]
        months, counts, avgs = process_issues(issues)
        self.assertEqual(months, ["2020-05"])
        self.assertEqual(counts, [2])
        self.assertAlmostEqual(avgs[0], 3.0)

    def test_multiple_months_and_open_issues(self):
        class Dummy:
            def __init__(self, c, x):
                self.created_date = c
                self.closed_date = x

        issues = [
            Dummy(datetime(2020, 4, 30), datetime(2020, 5, 2)),
            Dummy(datetime(2020, 5, 1), None),
            Dummy(datetime(2020, 5, 15), datetime(2020, 5, 20)),
            Dummy(datetime(2020, 6, 1), datetime(2020, 6, 10))
        ]
        months, counts, avgs = process_issues(issues)
        self.assertEqual(months, ["2020-04", "2020-05", "2020-06"])
        self.assertEqual(counts, [1, 2, 1])
        self.assertEqual(avgs, [2, 5, 9])

    def test_all_open_issues(self):
        class Dummy:
            def __init__(self, c, x):
                self.created_date = c
                self.closed_date = x

        issues = [
            Dummy(datetime(2021, 1, 1), None),
            Dummy(datetime(2021, 1, 5), None)
        ]
        months, counts, avgs = process_issues(issues)
        self.assertEqual(months, ["2021-01"])
        self.assertEqual(counts, [2])
        self.assertEqual(avgs, [0])

    def test_negative_resolution_time_bug(self):
        class Dummy:
            def __init__(self, c, x):
                self.created_date = c
                self.closed_date = x

        issues = [
            Dummy(datetime(2020, 5, 10), datetime(2020, 5, 5))
        ]
        months, counts, avgs = process_issues(issues)
        self.assertEqual(months, ["2020-05"])
        self.assertEqual(counts, [1])
        self.assertEqual(avgs[0], 0)

class TestRunFeature1WithMocks(unittest.TestCase):
    @patch("feature1_temporal_analysis.plt.show")
    @patch("feature1_temporal_analysis.plt.subplots")
    @patch("feature1_temporal_analysis.DataLoader")
    def test_run_feature_1_plots_correctly(self, mock_loader, mock_subplots, mock_show):
        class Dummy:
            def __init__(self, c, x):
                self.created_date = c
                self.closed_date = x

        mock_loader.return_value.get_issues.return_value = [
            Dummy(datetime(2020, 1, 1), datetime(2020, 1, 3)),
            Dummy(datetime(2020, 2, 1), None)
        ]

        fake_fig, fake_ax1 = MagicMock(), MagicMock()
        fake_ax2 = MagicMock()
        mock_subplots.return_value = (fake_fig, fake_ax1)
        fake_ax1.twinx.return_value = fake_ax2

        run_feature_1()

        fake_ax1.plot.assert_called_with(
            ["2020-01", "2020-02"], [1, 1],
            color="blue", marker="o", linewidth=1.5, label="No. of Issues Created"
        )
        fake_ax2.plot.assert_called_with(
            ["2020-01", "2020-02"], [2.0, 0],
            color="red", marker="x", linewidth=1.5, label="Average Days to Close"
        )
        fake_ax1.set_xlabel.assert_called_with("Month")
        fake_ax1.set_ylabel.assert_called_with("No. of Issues Created", color="blue")
        fake_ax2.set_ylabel.assert_called_with("Average Days to Close", color="red")
        mock_show.assert_called_once()

if __name__ == "__main__":
    unittest.main()
