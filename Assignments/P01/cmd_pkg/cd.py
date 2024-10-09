import sys
import os
from cmd_pkg.cmdsLogger import CmdsLogger 

def cd(**kwargs):
    cmds_Logger = CmdsLogger()
    sys.stdout = cmds_Logger

    try:
        input = kwargs["input"] if kwargs.get("input") else []
        params = kwargs["params"] if kwargs.get("params") else []
        flags = kwargs["flags"] if kwargs.get("flags") else []

        print('\r')

        if params:
            for param in params:
                try: 
                    param = param.replace("'", "").replace('"', "")
                    if param.startswith('~'):
                        os.chdir(os.path.expanduser("~"))
                    elif param == "..":
                        os.chdir("..")
                    else:
                        os.chdir(param)

                    print(f"Changed to directory: {os.getcwd()}")

                except FileNotFoundError:
                    print(f"Error: Directory '{param}' not found.")
                except PermissionError:
                    print(f"Error: Permission denied for directory '{param}'.")
                except Exception as e:
                    print(f"Error: {e}")
        else:
            os.chdir(os.path.expanduser("~"))  # Change to the home directory
            print(f"Changed to directory: {os.getcwd()}")

    finally:
        sys.stdout = sys.__stdout__

    captured_output = ''.join(cmds_Logger.log_content)
    return captured_output

