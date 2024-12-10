import sys
from helper_files.api_call import *
from helper_files.utils import *
from helper_files.cmdsLogger import PrintCaptureLogger
from colorama import Fore



def chmod(**kwargs):
    print_capture_logger = PrintCaptureLogger()
    sys.stdout = print_capture_logger

    try:
        params = kwargs["params"] if kwargs.get("params") else []
        flags = kwargs["flags"] if kwargs.get("flags") else []
        input = kwargs["input"] if kwargs.get("input") else []

        config = load_config()

        print('\r')

        try:
            if params and flags == [] and input ==[]:
                values = params[1:]
                mode = params[0]
                
                if not mode.isdigit() or len(mode) > 3 or not (0 <= int(mode[-2:], 8) <= 0o77):
                    raise Exception(f"mode must be an octal number between 00 and 77 for user and group: {mode}") 
    
                newPermVlu  = convert_mode_to_perm(mode)

                for param in values:
                    param = param.replace("'", "").replace('"', "")
                    permFile = get_file_permission(param,config['cwdid'])

                    if permFile["status_code"] == '200' and permFile["data"] is not None:
                        update_file_permission(param, config['cwdid'], newPermVlu)

                    permDir = get_dir_permission(param, config['cwdid'])
                    if permDir["status_code"] == '200' and permDir["data"] is not None:
                        update_dir_permission(param, config['cwdid'], newPermVlu)
                    
                    if permDir == [] and permFile == []:
                        raise Exception(f"{permDir["message"]}: {param}")      
                     
            elif input or flags:
                pass
            
            else:
                raise Exception(f"illegal command \nTry \'man chmod' for more information.")      

        except Exception as e:
            print(Fore.RED+f"chmod: {e}")
            
    finally:
        sys.stdout = sys.__stdout__  # Restore the original stdout

    captured_output = "".join(print_capture_logger.log_content)
    return captured_output 



