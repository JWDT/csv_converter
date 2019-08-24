
def func1(column_heading, line, previous_input_rows, previous_output_rows):
    val = line.get(column_heading)
    return int(val) * 2 if val.isdigit() else val
    

def func2(column_heading, line, previous_input_rows, previous_output_rows):
    val = line.get(column_heading)
    return int(val) * 10 if val.isdigit() else val
