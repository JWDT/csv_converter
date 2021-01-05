import csv
import io
import json
import logging
import importlib


class CSVConverter:
    config: dict
    previous_input_rows: list
    current_output_rows: list
    output_rows: list

    def refresh(self):
        self.previous_input_rows = []
        self.current_output_rows = []
        self.output_rows = []

    def __init__(self, config_json: str = None, config_file_name: str = None, config_dict: dict = None,
                 append_mode=False):
        """append_mode - used when appending multiple files across different sessions. This will not automatically
        run the self.refresh() command at the end of a conversion."""
        self.config = dict(config_dict) if config_dict else json.loads(config_json) if config_json else None
        self.append_mode = append_mode
        self.refresh()
        if not self.config:
            with open(config_file_name) as json_file:
                self.config = json.load(json_file)
        assert self.config
        if '$input_config$' in self.config:
            self.input_config = self.config.get('$input_config$') or {}
            del (self.config['$input_config$'])
        else:
            self.input_config = {}
        if '$output_config$' in self.config:
            self.output_config = self.config.get('$output_config$') or {}
            del (self.config['$output_config$'])
        else:
            self.output_config = {}
        logging.debug(f"Using config: {self.config}")
        self.output_headers = [header for header in self.config]

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
                # c above for c (it's defined in the exec line)
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

    def convert_dict_reader(self, input_dict: csv.DictReader):
        for line in input_dict:
            output_line = self._convert_line(line)
            self.output_rows.append(output_line)
            self.previous_input_rows.append(line)
            self.current_output_rows.append(output_line)
        return self.output_rows

    def xlsx_to_dict_reader(self, input_file_name: str):
        from openpyxl import load_workbook
        wb = load_workbook(filename=input_file_name, read_only=True)
        worksheets = []
        for ws in wb:
            rows = []
            for row in ws.rows:
                rows.append([cell.value for cell in row])
            csv_stringio = io.StringIO()
            csv.writer(csv_stringio).writerows(rows)
            csv_stringio.seek(0)
            if self.input_config.get('header_hints') or self.input_config.get('header_line_number'):
                pass
            worksheets.append(csv_stringio)
        for worksheet in worksheets:
            self.convert_dict_reader(csv.DictReader(worksheet))
        wb.close()

        pass

    def csv_to_dict_reader(self, input_file_name: str):
        if input_file_name.endswith(".xlsx") or str(self.input_config.get('format')).lower() == "xlsx":
            return self.xlsx_to_dict_reader(input_file_name)
        with open(input_file_name, 'r') as csv_file:
            csv_data = csv.DictReader(csv_file)
            return self.convert_dict_reader(csv_data)

    def convert(self, input_string=None, input_file_name=None, output_file_name=None):
        if input_string:
            raise NotImplementedError("input string not implemented yet.")
        input_files = [input_file_name] if type(input_file_name) is str else input_file_name
        with open(output_file_name, 'w+') if output_file_name else io.StringIO() as output_file:
            for input_file in input_files:
                self.csv_to_dict_reader(input_file)
            writer = csv.DictWriter(output_file, fieldnames=self.output_headers)
            writer.writeheader()
            writer.writerows(self.output_rows)
            output_file.seek(0)
            if not self.append_mode:
                self.refresh()
            return output_file.read()
