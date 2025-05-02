import unittest
from model import Issue, Event

class TestModel(unittest.TestCase):

    def test_issue_parsing_complete(self):
        sample = {
            "url": "http://example.com",
            "creator": "dev",
            "state": "closed",
            "created_at": "2022-01-01T12:00:00Z",
            "closed_at": "2022-01-05T12:00:00Z",
            "updated_at": "2022-01-06T12:00:00Z",
            "labels": [],
            "assignees": [],
            "title": "Test",
            "text": "Body",
            "number": 1,
            "timeline_url": "",
            "events": []
        }
        issue = Issue(sample)
        self.assertEqual(issue.url, "http://example.com")
        self.assertEqual(issue.state.name, "closed")
        self.assertEqual(issue.number, 1)

    def test_event_parsing_invalid_date(self):
        data = {"event_type": "comment", "event_date": "invalid-date"}
        event = Event(data)
        self.assertIsNone(event.event_date)

if __name__ == '__main__':
    unittest.main()
