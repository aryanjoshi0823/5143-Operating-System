import sys
from helper_files.api_call import *
from helper_files.utils import *
from helper_files.cmdsLogger import PrintCaptureLogger
from colorama import Fore



def mkdir(**kwargs):
    print_capture_logger = PrintCaptureLogger()
    sys.stdout = print_capture_logger

    try: 
        input = kwargs["input"] if kwargs.get("input") else []
        params = kwargs["params"] if kwargs.get("params") else []
        flags = kwargs["flags"] if kwargs.get("flags") else []

        config = load_config()

        print('\r')

        try:
            if params and input == [] and flags == []:
                for param in params:
                    param = param.replace("'", "").replace('"', "")
                    mkdir_res = make_directory(param,config['cwdid'])

                    if mkdir_res["status_code"] == '200' and mkdir_res["data"] is not None:
                        pass
            else:
                raise Exception("illegal option \nTry \'man mkdir' for more information.")

        except Exception as e:
            print(Fore.RED+f"mkdir: {e}")

    finally:
        sys.stdout = sys.__stdout__  # Restore the original stdout

    captured_output = ''.join(print_capture_logger.log_content)
    return captured_output

