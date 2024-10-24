import sys
from helper_files.api_call import *
from helper_files.utils import *

def sort(**kwargs):

    config = load_config()

    input = kwargs["input"] if kwargs.get("input") else []
    params = kwargs["params"] if kwargs.get("params") else []
    flags = kwargs["flags"] if kwargs.get("flags") else []

    try:
        is_reverse_order = 'r' in flags
        is_numeric_sort = 'n' in flags

        data = ""

        if params:
            for param in params:
                first_params = param.strip() 
                rfd = read_file_data(first_params,config['cwdid'])

                if rfd["status_code"] == '200' and rfd["data"] is not None:
                    data = data + rfd["data"]
                else:
                    print(rfd["message"] )
            
        elif input:
            data = input
        else:
            data = sys.stdin.read()
        
        # Split the input data into lines and sort them
        lines = data.splitlines()
        sorted_lines = sorted(lines, reverse = is_reverse_order, key=lambda x: int(x) if is_numeric_sort else x)

        sorted_output = "\n".join(sorted_lines)
        print('\n')
        print(sorted_output)
        return (str(sorted_output))

    except Exception as e:
        print(f"Error: {str(e)}")

    
