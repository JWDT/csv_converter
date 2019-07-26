import csv
import io
import json
import logging


class CSVConverter:
    config: dict
    def __init__(self, config_json: str = None, config_file: str = None, config_dict: dict = None):
        self.config = dict(config_dict) if config_dict else json.loads(config_json) if config_json else None
        if not self.config:
            with open(config_file) as json_file:
                self.config = json.load(json_file)
        assert self.config
        logging.debug(f"Using config: {self.config}")

    def _process_complex_column(self, line: csv.OrderedDict, item: dict):
        pass

    def _convert_line(self, line):
        output_line = csv.OrderedDict()
        for new_heading, item in self.config.items():
            if isinstance(item, str):
                item_output = line.get(item)
            else:
                item_output = self._process_complex_column(line, item)
            output_line.update({new_heading: item_output})
        # output_line = csv.OrderedDict({'Test': 'tval', 'Bla': 'Frog'})
        return output_line

    def convert(self, input_string=None, input_file_name=None, output_file_name=None):
        with open(input_file_name, 'r') as csv_file:
            output_rows = []
            csv_data = csv.DictReader(csv_file)
            for line in csv_data:
                output_line = self._convert_line(line)
                output_rows.append(output_line)
            fieldnames = []
            for header_name, _ in self.config.items():
                fieldnames.append(header_name)

            with open(output_file_name, 'w+') if output_file_name else io.StringIO() as output_file:
                writer = csv.DictWriter(output_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(output_rows)
                output_file.seek(0)
                return output_file.read()
