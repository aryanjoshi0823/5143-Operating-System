import sys
from helper_files.cmdsLogger import PrintCaptureLogger
from colorama import Fore


def remove_outer_quotes(param):
    # Check if the string starts and ends with the same quote (either ' or ")
    if (param.startswith('"') and param.endswith('"')) or (param.startswith("'") and param.endswith("'")):
        return param[1:-1]  # Remove the outermost quotes
    return param # Return as is if no outer quotes

def echo(**kwargs):
    print_capture_logger = PrintCaptureLogger()
    sys.stdout = print_capture_logger

    try:
        params = kwargs["params"] if kwargs.get("params") else []
        input = kwargs["input"] if kwargs.get("input") else []

        try:
            if params and input ==[]:
                cleaned_params = " ".join([remove_outer_quotes(p) for p in params]) 
                print(cleaned_params)

            elif input and params == []:
                cleaned_params = "".join([remove_outer_quotes(p) for p in input]) 
                print(cleaned_params)

        except Exception as e:
            print(Fore.RED+f"echo: {e}")
    
    finally:
        sys.stdout = sys.__stdout__  # Restore the original stdout

    captured_output = ''.join(print_capture_logger.log_content)
    return captured_output
