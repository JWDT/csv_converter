A simple tool that uses a JSON config file (or a config dict) to convert one CSV to another.

Simplest use case is to just list the new headers and link them to the old headers, like so:

```json
{
"New Column Header One": "Old Column Header One",
"New Column Header Two": "Old Column Header Two"
}
```

A slightly more useful version specifies a default to use (implemented using the "or" operator `value_from_old_column or default`):

```json
{
  "New Header One": {
    "old_column": "Old Header One",
    "default": "DEFAULT VALUE FOR ONE"
  },
  "New Header Two": {
    "old_column": "Old Header Two",
    "default": "DEFAULT VALUE FOR TWO"
  }
}
```

The third and final currently implemented option is to use a lambda function (use of full functions is planned):

```json
{
  "New Header One": {
    "old_column": "Old Header One",
    "default": "DEFAULT FOR ONE",
    "lambda": "lambda a, b: str(a.get(b.get('old_column'))).lower()"
  },
  "New Header Two": {
    "old_column": "Old Header Two",
    "default": "DEFAULT FOR TWO",
    "lambda": "lambda a, b: str(a.get(b.get('old_column'))).lower()"
  }
}
```

It will run the lambda as:

```python
item['lambda'] = "lambda a, b: str(a.get(b.get('old_column'))).lower()"
exec(f"c = {item.get('lambda')}", globals())
return c(line, item)
```

Where `line` is the current line of the source CSV, and `item` is the current element from the JSON file (the current column).

## Usage: 

```python
from csv_converter import CSVConverter
converter = CSVConverter(config_file_name='path-to-config.json')
output = converter.convert(input_file_name='path-to-source.csv')

# For multiple files, either feed them in as a list:
output = converter.convert(input_file_name=['path-to-file-one.csv', 'path-to-file-two.csv'])

#or re-use the same converter with the "append_mode" flag set to True -- this will make it remember all previous files
converter = CSVConverter(config_file_name='path-to-config.json', append_mode=True)
output_of_file_one = converter.convert(input_file_name='path-to-file-one.csv')
output_of_file_one_and_two = converter.convert(input_file_name='path-to-file-two.csv')

```


## Input Config

This goes at the same level as the headers, with the special name "$input_config$"

This supports setting the file format type. Useful if importing an xlsx file that for some reason doesn't have
the right filename. Use `format` for this.

Can also be used to specify which line the header is actually on.

`header_line_number` is one indexed to line up with the numbers on spreadsheet software.

`header_hints` is a list of strings that should match to help find the header.

If both are specified, it will start looking for the header line on the line specified.

```json
{
  "$input_config$": {
      "format": "xlsx", // "ods" to be supported later.
      "header_line_number": 3,
      "header_hints": ["Old Header Zero", "Old Header One"],
      "header_hints_in_order": null, // not implemented yet
      "header_hints_together": null // not implemented yet
  },
  "New Header Zero": {
    "old_column": "Old Header Zero",
    "default": "DEFAULT FOR ZERO"
  }
}
```