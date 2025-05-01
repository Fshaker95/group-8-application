
import unittest
import os
import tempfile
import config

class TestConfig(unittest.TestCase):
    def test_get_parameter_from_env(self):
        os.environ['ENPM611_TEST_PARAM'] = 'env_value'
        value = config.get_parameter('ENPM611_TEST_PARAM')
        self.assertEqual(value, 'env_value')
        del os.environ['ENPM611_TEST_PARAM']

    def test_get_parameter_from_config(self):
        value = config.get_parameter('ENPM611_PROJECT_DATA_PATH')
        self.assertIsNotNone(value)

    def test_get_parameter_with_default(self):
        value = config.get_parameter('NONEXISTENT_PARAM', default='default_value')
        self.assertEqual(value, 'default_value')

    def test_set_parameter(self):
        config.set_parameter('TEMP_PARAM', 'temp_value')
        self.assertEqual(config.get_parameter('TEMP_PARAM'), 'temp_value')

    def test_convert_to_typed_value_json_string(self):
        self.assertEqual(config.convert_to_typed_value('{"key": "value"}'), {"key": "value"})

    def test_convert_to_typed_value_non_json(self):
        self.assertEqual(config.convert_to_typed_value('simple_string'), 'simple_string')

    def test_init_config_no_file(self):
        temp_dir = tempfile.gettempdir()
        current = os.getcwd()
        try:
            os.chdir(temp_dir)  # Go to system temp directory
            config._config = None  # Force reinit
            config._init_config()
            self.assertIsInstance(config._config, dict)
        finally:
            os.chdir(current)
