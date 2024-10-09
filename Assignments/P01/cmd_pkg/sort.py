import os
import sys

def sort(**kwargs):
    try:
        is_reverse_order = 'r' in kwargs["flags"]
        is_numeric_sort = 'n' in kwargs["flags"]

        if kwargs["params"]:
            first_params = kwargs["params"][0]
            if os.path.isfile(first_params):
                with open(first_params,'r') as file:
                    data = file.read()
            else:
                raise FileNotFoundError(f"File '{first_params}' not found.")
            
        elif kwargs["input"] != []:
            data = kwargs["input"]
        else:
            data = sys.stdin.read()
        
        # Split the input data into lines and sort them
        lines = data.splitlines()
        sorted_lines = sorted(lines, reverse = is_reverse_order, key=lambda x: int(x) if is_numeric_sort else x)

        sorted_output = "\n".join(sorted_lines)
        print('\n')
        print(sorted_output)
        return ""

    except Exception as e:
        print(f"Error: {str(e)}")

    
