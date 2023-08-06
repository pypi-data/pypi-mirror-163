import os
import uuid
import quickbe
import unittest
import quickbe.utils as ut


class UtilsTestCase(unittest.TestCase):

    def test_get_env_var_as_int(self):
        test_cases = {
            1: 1,
            2: 2.1,
            3: '3'
        }
        for expected_val, value in test_cases.items():
            name = f'var_{uuid.uuid4()}'
            self.assertEqual(expected_val, quickbe.get_env_var_as_int(key=name, default=value))
            os.environ[name] = str(value)
            self.assertEqual(expected_val, quickbe.get_env_var_as_int(key=name))

    def test_remove_suffix(self):
        test_cases = {
            'hello world': 'hello ',
            'world hello world': 'world hello ',
            'hello world ': 'hello world ',
        }
        for value, expected_val in test_cases.items():
            self.assertEqual(expected_val, quickbe.remove_suffix(s=value, suffix='world'))

    def test_generate_token(self):
        self.assertEqual(32, len(ut.generate_token()))
        self.assertEqual(64, len(ut.generate_token(length=64)))
        translate_table = ''.maketrans("abc", "***")
        self.assertEqual('**********', ut.generate_token(chars='abc', length=10).translate(translate_table))


if __name__ == '__main__':
    unittest.main()
