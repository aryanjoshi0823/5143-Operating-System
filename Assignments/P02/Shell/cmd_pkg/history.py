""" Methods written to implement the shell command 'History'. """
from helper_files.api_call import *
from helper_files.utils import *

from cmd_pkg.cmdsLogger import CmdsLogger


commands_history = []

def add_commands_to_history(commands, flags):
    try:
        if commands.strip():
            commands_history.append(commands.strip())
    except Exception as e:
        print("An error occurred:", e)
    
     # Returns the updated history and the index of the last added command
    return commands_history, (len(commands_history)-1)

def history(**kwargs):
    """Display history of command executed in current session."""

    try:
        print("\n")
        if "params" in kwargs:
            params = kwargs["params"] 
        else:
            params = ["."]

        if "flags" in kwargs:
            flags = kwargs["flags"]
            if '--help' in flags:
                help_text = """ """
        else:
            flags = []

        # rd = read_file_data("History", 6)
        # if rd["status_code"] == '200' and rd["data"] is not None:
        #     his_vlu = rd["data"].split("\n")
        #     for each_cmd in his_vlu:
        #         print(each_cmd)
        # else:
        #     print(f"{rd["message"]}")

        for x in commands_history:
            print(x)

        print(commands_history)
        return(str(commands_history))


    except Exception as e:
        print("An error occurred while displaying history:", e)


