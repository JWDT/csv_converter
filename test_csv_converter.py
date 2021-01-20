import json
import os
import unittest

from csv_converter import CSVConverter

fo = 'test_files'


class MyTestCase(unittest.TestCase):
    def test_error_if_no_config(self):
        with self.assertRaises(Exception):
            CSVConverter(config_json=None, config_file_name=None, config_dict=None)
        with self.assertRaises(Exception):
            CSVConverter()

    def test_error_if_bad_config(self):
        with self.assertRaises(Exception):
            CSVConverter(config_json='Not real valid JSON here...')
        with self.assertRaises(Exception):
            CSVConverter(config_file_name=os.path.join(fo, 'non-existant-file-hfhffhjksdfhjksfhjk'))
        with self.assertRaises(Exception):
            CSVConverter(config_file_name=os.path.join(fo, 'real-but-invalid.json'))
        with self.assertRaises(Exception):
            # noinspection PyTypeChecker
            CSVConverter(config_dict=['This isn', 't a dict'])

    def test_simple_case(self):
        converter = CSVConverter(config_file_name=os.path.join(fo, 'valid-simple-header-change.json'))
        output = converter.convert(input_file_name=os.path.join(fo, 'valid-simple.csv'))
        with open(os.path.join(fo, 'valid-simple-new.csv')) as output_file:
            self.assertEqual(output_file.read(), output.replace('\r\n', '\n'))

    def test_simple_case_twice_no_append(self):
        converter = CSVConverter(config_file_name=os.path.join(fo, 'valid-simple-header-change.json'))
        output = converter.convert(input_file_name=os.path.join(fo, 'valid-simple.csv'))
        with open(os.path.join(fo, 'valid-simple-new.csv')) as output_file:
            self.assertEqual(output_file.read(), output.replace('\r\n', '\n'))
        output = converter.convert(input_file_name=os.path.join(fo, 'valid-simple.csv'))
        with open(os.path.join(fo, 'valid-simple-new.csv')) as output_file:
            self.assertEqual(output_file.read(), output.replace('\r\n', '\n'))

    def test_simple_case_twice_with_append(self):
        converter = CSVConverter(config_file_name=os.path.join(fo, 'valid-simple-header-change.json'), append_mode=True)
        output = converter.convert(input_file_name=os.path.join(fo, 'valid-simple.csv'))
        with open(os.path.join(fo, 'valid-simple-new.csv')) as output_file:
            self.assertEqual(output_file.read(), output.replace('\r\n', '\n'))
        output = converter.convert(input_file_name=os.path.join(fo, 'valid-simple-two.csv'))
        with open(os.path.join(fo, 'valid-simple-appended.csv')) as output_file:
            self.assertEqual(output_file.read(), output.replace('\r\n', '\n'))

    def test_simple_out_of_order_case(self):
        converter = CSVConverter(config_file_name=os.path.join(fo, 'valid-simple-header-change.json'))
        output = converter.convert(input_file_name=os.path.join(fo, 'valid-simple-out-of-order.csv'))
        with open(os.path.join(fo, 'valid-simple-new.csv')) as output_file:
            self.assertEqual(output_file.read(), output.replace('\r\n', '\n'))

    def test_simple_with_defaults(self):
        converter = CSVConverter(config_file_name=os.path.join(fo, 'valid-simple-with-defaults.json'))
        output = converter.convert(input_file_name=os.path.join(fo, 'valid-simple-with-missing.csv'))
        with open(os.path.join(fo, 'valid-simple-with-defaults.csv')) as output_file:
            self.assertEqual(output_file.read(), output.replace('\r\n', '\n'))

    def test_simple_with_lambda(self):
        converter = CSVConverter(config_file_name=os.path.join(fo, 'valid-simple-with-lambda.json'))
        output = converter.convert(input_file_name=os.path.join(fo, 'valid-simple.csv'))
        with open(os.path.join(fo, 'valid-simple-to-lower.csv')) as output_file:
            self.assertEqual(output_file.read(), output.replace('\r\n', '\n'))

    def test_simple_with_funlinks(self):
        converter = CSVConverter(config_file_name=os.path.join(fo, 'valid-simple-with-funlink.json'))
        output = converter.convert(input_file_name=os.path.join(fo, 'valid-simple.csv'))
        with open(os.path.join(fo, 'valid-simple-double-digits.csv')) as correct_file:
            self.assertEqual(correct_file.read(), output.replace('\r\n', '\n'))

    def test_append_two_simple(self):
        converter = CSVConverter(config_file_name=os.path.join(fo, 'valid-simple-header-change.json'))
        output = converter.convert(input_file_name=[os.path.join(fo, 'valid-simple.csv'),
                                                    os.path.join(fo, 'valid-simple-two.csv')])
        with open(os.path.join(fo, 'valid-simple-appended.csv')) as correct_file:
            self.assertEqual(correct_file.read(), output.replace('\r\n', '\n'))

    def test_xlsx_simple(self):
        converter = CSVConverter(config_file_name=os.path.join(fo, 'valid-simple-header-change.json'))
        output = converter.convert(input_file_name=os.path.join(fo, 'valid-simple.xlsx'))
        with open(os.path.join(fo, 'valid-simple-new.csv')) as output_file:
            self.assertEqual(output_file.read(), output.replace('\r\n', '\n'))

    def test_simple_case_with_junk_before_heading(self):
        converter = CSVConverter(config_file_name=os.path.join(fo, 'valid-simple-header-change-with-hints.json'))
        output = converter.convert(input_file_name=os.path.join(fo, 'valid-simple-with-junk-before-heading.csv'))
        with open(os.path.join(fo, 'valid-simple-new.csv')) as output_file:
            self.assertEqual(output_file.read(), output.replace('\r\n', '\n'))

    def test_xlsx_simple_case_with_junk_before_heading(self):
        converter = CSVConverter(config_file_name=os.path.join(fo, 'valid-simple-header-change-with-hints.json'))
        output = converter.convert(input_file_name=os.path.join(fo, 'valid-simple-with-junk-before-heading.xlsx'))
        with open(os.path.join(fo, 'valid-simple-new.csv')) as output_file:
            self.assertEqual(output_file.read(), output.replace('\r\n', '\n'))

    def test_simple_autogenerated_from_csv(self):
        output = CSVConverter(no_config=True).generate_json_headers(input_file_name=os.path.join(fo, 'valid-simple.csv'))
        with open(os.path.join(fo, 'valid-simple-autogenerated.json')) as output_file:
            self.assertEqual(json.load(output_file), output)


if __name__ == '__main__':
    unittest.main()
