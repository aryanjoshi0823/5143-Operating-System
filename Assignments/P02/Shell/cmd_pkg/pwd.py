from helper_files.utils import *
from helper_files.api_call import *

def pwd(**kwargs):

    """
     Print the name of the current working directory.
    """
    config = load_config()
    print('\r')
    if config["cwd"] == "" and config["root_or_home"] == '/':
        print("/root")
    elif config["cwd"] == "" and config["root_or_home"] == '~':
        try: 
            vlu = get_dir(config["cwdid"])
            if vlu["status_code"] == '200' and vlu["data"] is not None:
                print(f"/{vlu["data"][3]}")
        except Exception as e:
            print(f"Error: {e}")
            
    print(config["cwd"])
 


