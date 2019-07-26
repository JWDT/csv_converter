import csv
import io
import json
import logging


class CSVConverter:
    config: dict

    def __init__(self, config_json: str = None, config_file_name: str = None, config_dict: dict = None):
        self.config = dict(config_dict) if config_dict else json.loads(config_json) if config_json else None
        if not self.config:
            with open(config_file_name) as json_file:
                self.config = json.load(json_file)
        assert self.config
        if '$input_config$' in self.config:
            self.input_config = self.config.get('$input_config$')
            del(self.config['$input_config$'])
        if '$output_config$' in self.config:
            self.output_config = self.config.get('$output_config$')
            del(self.config['$output_config$'])
        logging.debug(f"Using config: {self.config}")

    def _process_complex_column(self, line: csv.OrderedDict, item: dict):
        logging.basicConfig(level=logging.DEBUG)
        built_in_processors = {
            "old_column": lambda a, b: a.get(b.get('old_column')) or None,
            "default, old_column": lambda a, b: a.get(b.get('old_column')) or b.get('default'),
            "default, lambda, old_column": None,
            "default, lambda": None,
            "lambda": None,
            "lambda, old_column": None,
        }
        keys = list(item.keys())
        keys.sort()
        process_type = ', '.join(keys)
        logging.debug(f"Process type: {process_type}")
        if process_type in built_in_processors:
            if "lambda" in item.keys():
                try:
                    exec(f"c = {item.get('lambda')}", globals())
                    return c(line, item)
                except:
                    process_type = "default, old_column" if "default" in process_type else "old_column"
            return built_in_processors[process_type](line, item)
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
