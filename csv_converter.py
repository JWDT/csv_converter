import csv
import io
import json
import logging
import importlib

class CSVConverter:
    config: dict

    def __init__(self, config_json: str = None, config_file_name: str = None, config_dict: dict = None):
        self.config = dict(config_dict) if config_dict else json.loads(config_json) if config_json else None
        self.previous_input_rows = []
        self.current_output_rows = []
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

    def _process_func_link(self, new_heading: str, line: csv.OrderedDict, mod_func_str: str):
        module_name, func_name = mod_func_str.split('/')
        module = importlib.import_module(module_name)
        func = getattr(module, func_name)
        return func(new_heading, line, self.previous_input_rows, self.current_output_rows)

    def _process_complex_column(self, column_heading: str, line: csv.OrderedDict, item: dict):
        logging.basicConfig(level=logging.DEBUG)

        # the dict can have have these keys: old_column, default, lambda, funlink
        item_output = None
        if 'old_column' in item:
            item_output = line.get(item.get('old_column')) or None

        if 'funlink' in item:
            mod_func_string = item.get('funlink')
            item_output = self._process_func_link(column_heading, line, mod_func_string)
        elif 'lambda' in item:
            try:
                exec(f"c = {item.get('lambda')}", globals())
                item_output = c(line, item)
            except:
                pass
        
        if item_output is None:
            item_output = item.get('default')

        return item_output

    def _convert_line(self, line):
        output_line = csv.OrderedDict()
        for new_heading, options in self.config.items():
            if isinstance(options, str):
                item_output = line.get(options)
            else:
                column_heading = options.get('old_column') if 'old_column' in options else new_heading
                item_output = self._process_complex_column(column_heading, line, options)
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
                self.previous_input_rows.append(line)
                self.current_output_rows.append(output_line)
            fieldnames = []
            for header_name, _ in self.config.items():
                fieldnames.append(header_name)

            with open(output_file_name, 'w+') if output_file_name else io.StringIO() as output_file:
                writer = csv.DictWriter(output_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(output_rows)
                output_file.seek(0)
                return output_file.read()
