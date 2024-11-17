import sys
from helper_files.api_call import get_directory_id
from helper_files.utils import load_config, save_config
from helper_files.cmdsLogger import PrintCaptureLogger
from colorama import Fore


def normalize_path(path, current_dir):
    # Split the path into components
    components = path.split('/')
    result_path = current_dir.split('/') if current_dir else []

    for part in components:
        if part == '..':
            if result_path:
                result_path.pop()  # Go to the parent directory
        elif part == '.' or part == '':
            continue  
        else:
            result_path.append(part) 

    # Join the result path to create the final normalized path
    normalized_path = '/'.join(result_path)
    if not normalized_path.startswith('/'):
        normalized_path = '/' + normalized_path  # check it's absolute
    return normalized_path

def cd(**kwargs):
    print_capture_logger = PrintCaptureLogger()
    sys.stdout = print_capture_logger

    try: 
        params = kwargs["params"] if kwargs.get("params") else []
        flags = kwargs["flags"] if kwargs.get("flags") else []
        input = kwargs["input"] if kwargs.get("input") else []

        config = load_config()

        print('\r')

        try:
            if len(params) > 1:
                raise Exception("more then one path") 

            elif params and flags == [] and input ==[]:

                for param in params:
                    param = param.replace("'", "").replace('"', "")
                    dir_res = get_directory_id(param,config['cwdid'])

                    if dir_res["status_code"] == '200' and dir_res["data"] is not None:
                        if dir_res["data"] == 0:
                            config["cwd"] = ""
                            config["cwdid"] = dir_res["data"] 
                            config["root_or_home"] = "/"

                        elif dir_res["data"] == 1:
                            config["cwd"] = ""
                            config["cwdid"] = dir_res["data"] 
                            config["root_or_home"] = "~" 

                        else:
                            normalized_path = normalize_path(param, config["cwd"])

                            config["cwd"] = normalized_path
                            config["cwdid"] = dir_res["data"]

                            # Handle paths starting with ~ or /
                            if param.startswith("~/"):
                                config["root_or_home"] = "~"
                                config["cwd"] = config["cwd"].replace("~/", "") 
                                
                        save_config(config)
                    else:
                        raise Exception(f"{dir_res['message']}") 

            elif input or flags:
                raise Exception(f"string not in pwd: {flags or input}") 
            
            else:
                raise Exception("illegal command \nTry \'man cd' for more information.") 
                
        except Exception as e:
            print(Fore.RED + f"cd: {e}")

    finally:
        sys.stdout = sys.__stdout__  # Restore the original stdout

    captured_output = ''.join(print_capture_logger.log_content)
    return captured_output
        


