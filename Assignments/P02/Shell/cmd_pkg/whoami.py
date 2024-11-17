from helper_files.api_call import *
from helper_files.utils import *
from helper_files.cmdsLogger import PrintCaptureLogger
import sys



def whoami(**kwargs):
    print_capture_logger = PrintCaptureLogger()
    sys.stdout = print_capture_logger

    try:
        input = kwargs["input"] if kwargs.get("input") else []
        params = kwargs["params"] if kwargs.get("params") else []
        flags = kwargs["flags"] if kwargs.get("flags") else []

        if params and input and flags:
            pass
        else:
            config = load_config()
            print(config["user"])
    finally:
        sys.stdout = sys.__stdout__  

    captured_output = ''.join(print_capture_logger.log_content)
    return captured_output



