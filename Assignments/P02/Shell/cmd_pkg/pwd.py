

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
        current_dir=os.getcwd()
        print(current_dir)
    finally:
            sys.stdout = sys.__stdout__  # Restore the original stdout

    captured_output = ''.join(cmd_capture_logger.log_content)
    return captured_output  
