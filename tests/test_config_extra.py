
import unittest
import config

class TestConfigExtra(unittest.TestCase):
    def test_overwrite_from_args(self):
        class Args:
            def __init__(self):
                self.test_param = 'arg_value'
        args = Args()
        config.overwrite_from_args(args)
        self.assertEqual(config.get_parameter('test_param'), 'arg_value')

if __name__ == '__main__':
    unittest.main()
