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
        with self.assertRaises(Exception):
            # noinspection PyTypeChecker
            CSVConverter(config_dict=['This isn', 't a dict'])

    def test_simple_case(self):
        converter = CSVConverter(config_file=os.path.join(fo, 'valid-simple-header-change.json'))
        output = converter.convert(input_file_name=os.path.join(fo, 'valid-simple.csv'))
        with open(os.path.join(fo, 'valid-simple-new.csv')) as output_file:
            self.assertEqual(output_file.read(), output.replace('\r\n', '\n'))


if __name__ == '__main__':
    unittest.main()
