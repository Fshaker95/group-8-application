import unittest
import os
import tempfile
import json
import config

class TestConfig(unittest.TestCase):

    def setUp(self):
        config._config = None  # reset before each test

    def tearDown(self):
        if os.path.exists('config.json'):
            os.remove('config.json')
        config._config = None

    def test_get_parameter_from_env(self):
        os.environ['ENPM611_TEST_PARAM'] = 'env_value'
        value = config.get_parameter('ENPM611_TEST_PARAM')
        self.assertEqual(value, 'env_value')
        del os.environ['ENPM611_TEST_PARAM']

    def test_get_parameter_from_config(self):
        with open('config.json', 'w') as f:
            json.dump({"ENPM611_PROJECT_DATA_PATH": "some_path.json"}, f)
        value = config.get_parameter('ENPM611_PROJECT_DATA_PATH')
        self.assertEqual(value, "some_path.json")

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
            os.chdir(temp_dir)  # Go to a directory without config.json
            config._config = None
            config._init_config()
            self.assertIsInstance(config._config, dict)
        finally:
            os.chdir(current)

    def test_get_default_path_success(self):
        # Create a config.json in the current dir
        with open('config.json', 'w') as f:
            json.dump({"EXISTING_PARAM": "file_value"}, f)
        config._config = None
        path = config._get_default_path()
        self.assertTrue(path.endswith('config.json'))

    def test_init_config_invalid_json(self):
        with open('config.json', 'w') as f:
            f.write('{ bad json }')
        config._config = None
        with self.assertRaises(json.JSONDecodeError):
            config._init_config()

    def test_overwrite_from_args(self):
        class DummyArgs:
            def __init__(self):
                self.param1 = "value1"
                self.param2 = None

        dummy = DummyArgs()
        config.overwrite_from_args(dummy)
        self.assertEqual(os.environ.get('param1'), 'value1')

if __name__ == "__main__":
    unittest.main()
