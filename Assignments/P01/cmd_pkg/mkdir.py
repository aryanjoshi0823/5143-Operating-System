import sys
import os
import errno 
from cmd_pkg.cmdsLogger import CmdsLogger
import traceback

def create_dir(path):
    try:
        os.makedirs(path)
        print(f"Created directory: {path}")

    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            print(f"Directory already exists: {path}")
        else:
            print("Error")
            traceback.print_exc() 


def mkdir(**kwargs):

    cmds_logger = CmdsLogger()
    sys.stdout = cmds_logger

    try:
        input = kwargs["input"] if kwargs.get("input") else []
        params = kwargs["params"] if kwargs.get("params") else []
        flags = kwargs["flags"] if kwargs.get("flags") else []

        print('\n')
        
        if params:
            for param in params:
                param = param.replace("'", "").replace('"', "")

                if flags:
                    if not os.path.isabs(param):
                        curr_dir = os.getcwd()
                        new_dir = os.path.join(curr_dir, param)
                    else:
                        new_dir = param
                    create_dir(new_dir)
                else:
                    if os.path.isabs(param):
                        if os.path.exists(param):
                            print(f"Directory already exists: {param}")
                        else:
                            create_dir(param)
                    else:
                        try:
                            os.mkdir(param)
                            print(f"Created directory: {param}")
                        except FileExistsError:
                            print(f"Directory already exists: {param}")
                        except FileNotFoundError:
                            print(f"Directory does not exists: {param}")
        else:
            print("mkdir: missing operand \nTry \'mkdir --help' for more information.")
            
    finally:
        sys.stdout = sys.__stdout__
    
    captured_output = ''.join(cmds_logger.log_content)
    return captured_output

