import os
import unittest

from csv_converter import CSVConverter

fo = 'test_files'


class MyTestCase(unittest.TestCase):
    def test_error_if_no_config(self):
        with self.assertRaises(Exception):
            CSVConverter(config_json=None, config_file=None, config_dict=None)
        with self.assertRaises(Exception):
            CSVConverter()

    def test_error_if_bad_config(self):
        with self.assertRaises(Exception):
            CSVConverter(config_json='Not real valid JSON here...')
        with self.assertRaises(Exception):
            CSVConverter(config_file=os.path.join(fo, 'non-existant-file-hfhffhjksdfhjksfhjk'))
        with self.assertRaises(Exception):
            CSVConverter(config_file=os.path.join(fo, 'real-but-invalid.json'))
    # def test_simple_case(self):
    #     self.assertEqual()

if __name__ == '__main__':
    unittest.main()
