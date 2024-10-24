
from helper_files.api_call import *
from helper_files.utils import *

def mkdir(**kwargs):
    input = kwargs["input"] if kwargs.get("input") else []
    params = kwargs["params"] if kwargs.get("params") else []
    flags = kwargs["flags"] if kwargs.get("flags") else []

    config = load_config()

    print('\r')

    if params:
        try:
            for param in params:
                param = param.replace("'", "").replace('"', "")
                mkdir_res = make_directory(param,config['cwdid'])

                if mkdir_res["status_code"] == '200' and mkdir_res["data"] is not None:
                    print("Directory Created.")
    
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("mkdir: missing operand \nTry \'mkdir --help' for more information.")

