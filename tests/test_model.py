
import unittest
from model import Issue, Event

class TestModel(unittest.TestCase):
    def test_issue_from_valid_json(self):
        jobj = {
            'url': 'https://example.com',
            'creator': 'testuser',
            'labels': [{'name': 'bug'}],
            'state': 'open',
            'number': '1',
            'created_at': '2024-01-01T12:00:00Z',
            'closed_at': '2024-01-02T12:00:00Z',
            'updated_at': '2024-01-03T12:00:00Z',
            'events': [{'event_type': 'commented', 'author': 'bob', 'event_date': '2024-01-01T12:30:00Z'}]
        }
        issue = Issue(jobj)
        self.assertEqual(issue.creator, 'testuser')
        self.assertIn('bug', issue.labels)
        self.assertEqual(issue.state, 'open')
        self.assertEqual(issue.number, 1)
        self.assertEqual(len(issue.events), 1)

    def test_event_from_partial_json(self):
        jobj = {'event_type': 'closed'}
        event = Event(jobj)
        self.assertEqual(event.event_type, 'closed')
        self.assertIsNone(event.author)

    def test_issue_handles_missing_fields(self):
        issue = Issue({'state': 'open'})  # Provide at least a minimal valid state
        self.assertIsNone(issue.creator)
        self.assertEqual(issue.number, -1)
