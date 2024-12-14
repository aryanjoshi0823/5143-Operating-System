import sys
from helper_files.api_call import *
from helper_files.utils import *
from helper_files.cmdsLogger import PrintCaptureLogger
from colorama import Fore


def sort(**kwargs):
    print_capture_logger = PrintCaptureLogger()
    sys.stdout = print_capture_logger

    try:

        config = load_config()

        input = kwargs["input"] if kwargs.get("input") else []
        params = kwargs["params"] if kwargs.get("params") else []
        flags = kwargs["flags"] if kwargs.get("flags") else []

        try:
            is_reverse_order = 'r' in flags
            is_numeric_sort = 'n' in flags

            data = ""

            if params and input == []:
                for param in params:
                    vlu_params = param.strip() 
                    rfd = read_file_data(vlu_params,config['cwdid'])

                    if rfd["status_code"] == '200' and rfd["data"] is not None:
                        data = data + rfd["data"]
                    else:
                        raise Exception(rfd["message"] )
                
            elif input and params == []:
                data = input

            else:
                data = sys.stdin.read()
            
            # Split the input data into lines and sort them
            lines = data.splitlines()
            sorted_lines = sorted(lines, reverse = is_reverse_order, key=lambda x: int(x) if is_numeric_sort else x)

            sorted_output = "\n".join(sorted_lines)
            print('\n')
            print(sorted_output)

        except Exception as e:
            print(Fore.RED+f"sort: {str(e)}")

    finally:
        sys.stdout = sys.__stdout__  # Restore the original stdout

    captured_output = "".join(print_capture_logger.log_content)
    return captured_output 

    
