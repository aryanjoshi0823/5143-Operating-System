from helper_files.api_call import *
from helper_files.utils import *

def chmod(**kwargs):

    input = kwargs["input"] if kwargs.get("input") else []
    params = kwargs["params"] if kwargs.get("params") else []
    flags = kwargs["flags"] if kwargs.get("flags") else []

    config = load_config()

    print('\r')
    #/python_code/ShapeModules/Point.pyc  
    if params:
        try:
            values = params[1:]
            mode = params[0]
            
            if not mode.isdigit() or len(mode) > 3 or not (0 <= int(mode[-2:], 8) <= 0o77):
                print("Error: Mode must be an octal number between 00 and 77 for user and group.")
                return
 
            newPermVlu  = convert_mode_to_perm(mode)

            for param in values:
                param = param.replace("'", "").replace('"', "")
                permFile = get_file_permission(param,config['cwdid'])

                if permFile["status_code"] == '200' and permFile["data"] is not None:
                    update_file_permission(param, config['cwdid'], newPermVlu)

                permDir = get_dir_permission(param, config['cwdid'])
                if permDir["status_code"] == '200' and permDir["data"] is not None:

                    dir_res = update_dir_permission(param, config['cwdid'], newPermVlu)
                    print(dir_res)
                print("permDir---",permDir)

        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Error:  Please provide at least one MODE and one FILE.")

    



