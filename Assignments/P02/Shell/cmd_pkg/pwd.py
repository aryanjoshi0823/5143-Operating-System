import sys
from helper_files.utils import *
from helper_files.api_call import *
from helper_files.cmdsLogger import PrintCaptureLogger
from colorama import Fore



def pwd(**kwargs):
    print_capture_logger = PrintCaptureLogger()
    sys.stdout = print_capture_logger

    try:
        params = kwargs["params"] if kwargs.get("params") else []
        flags = kwargs["flags"] if kwargs.get("flags") else []
        input = kwargs["input"] if kwargs.get("input") else []
    
        config = load_config()

        try:
            if params or flags or input:
                pass
            else:
                print('\r')
                if config["cwd"] == "" and config["root_or_home"] == '/':
                    print("/root")
                elif config["cwd"] == "" and config["root_or_home"] == '~':
                    vlu = get_dir(config["cwdid"])
                    if vlu["status_code"] == '200' and vlu["data"] is not None:
                        print(f"/{vlu["data"][3]}")
                        
                print(config["cwd"])

        except Exception as e:
            print(Fore.RED+f"pwd: {e}")

    finally:
        sys.stdout = sys.__stdout__  # Restore the original stdout

    captured_output = "".join(print_capture_logger.log_content)
    return captured_output 
 


