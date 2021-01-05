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
