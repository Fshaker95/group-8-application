import unittest
import tempfile
import json
import os
from data_loader import DataLoader
import config

class TestDataLoader(unittest.TestCase):

    def test_load_valid_file(self):
        sample = [{"url": "http://example.com", "state": "closed", "created_at": "2022-01-01T00:00:00Z"}]
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as tf:
            json.dump(sample, tf)
            tf.flush()
            os.environ['ENPM611_PROJECT_DATA_PATH'] = tf.name
            config._config = None  # reset config
            loader = DataLoader()
            issues = loader.get_issues()
            self.assertTrue(len(issues) > 0)
        os.unlink(tf.name)

    def test_missing_file(self):
        os.environ['ENPM611_PROJECT_DATA_PATH'] = 'non_existent.json'
        config._config = None  # reset config
        loader = DataLoader()
        with self.assertRaises(FileNotFoundError):
            loader._load()

if __name__ == '__main__':
    unittest.main()
