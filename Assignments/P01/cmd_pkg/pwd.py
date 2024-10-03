

import os
import sys
from cmd_pkg.cmdsLogger import CmdsLogger

def pwd(**kwargs):

    """
     Print the name of the current working directory.
    """
    cmd_capture_logger = CmdsLogger()
    sys.stdout = cmd_capture_logger
    try:
        # input = kwargs["input"] if "input" in kwargs else []
        # if "params" in kwargs:
        #     params = kwargs["params"] if kwargs.get("params") else []
        # else:
        #     params = []
        # if "flags" in kwargs:
        #     flags = kwargs["flags"]
        # else:
        #     flags = []
        current_dir=os.getcwd()
       # print("\r")
        print(current_dir)
    finally:
            sys.stdout = sys.__stdout__  # Restore the original stdout

    captured_output = ''.join(cmd_capture_logger.log_content)
    return captured_output  
