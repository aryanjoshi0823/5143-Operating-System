import sys
from helper_files.api_call import *
from helper_files.utils import *
from helper_files.cmdsLogger import PrintCaptureLogger
from colorama import Fore


commands_history = []

def populate_cmd_history():
    get_cmds_vlu = getCmds()
    if get_cmds_vlu is None:
        return
    elif get_cmds_vlu["status_code"] == '200' and get_cmds_vlu["data"] is not None:
        data_rd = get_cmds_vlu["data"]

        if commands_history:
            latest_entry_id = commands_history[-1][0]  
            new_entries = [cmd for cmd in data_rd if cmd[0] > latest_entry_id]
        else:
            new_entries = data_rd
        
        for cmd in new_entries:
            commands_history.append(cmd)
            
populate_cmd_history()

def add_commands(commands, flags):
    try:
        if commands:
            post_cmds = update_history(commands)
            if post_cmds["status_code"] == '200':
                populate_cmd_history()
    except Exception as e:
        print(Fore.RED+f"history:{e}")

     # Returns the updated history and the index of the last added command
    return commands_history, (len(commands_history)-1)

def history(**kwargs):
    print_capture_logger = PrintCaptureLogger()
    sys.stdout = print_capture_logger
    try:
        """Display history of command executed in current session."""
        params = kwargs["params"] if kwargs.get("params") else []
        flags = kwargs["flags"] if kwargs.get("flags") else []
        input = kwargs["input"] if kwargs.get("input") else []


        try:
            print("\n")
            if params or flags or input:
                pass

            else:
                get_cmds_vlu = getCmds()
                if get_cmds_vlu["status_code"] == '200' and get_cmds_vlu["data"] is not None:
                    data = get_cmds_vlu["data"]
                    for eachCmds in data:
                        print(f"{eachCmds[0]} {eachCmds[1]} {format_time(eachCmds[2])}")
                else:
                    raise Exception(f"{get_cmds_vlu["message"]}") 
     
        except Exception as e:
            print(Fore.RED+f"history:{e}")
    finally:
        sys.stdout = sys.__stdout__  # Restore the original stdout

    captured_output = "".join(print_capture_logger.log_content)
    return captured_output 

def cmds_from_history(cmds):
    if cmds.startswith('!'):
        try:
            print('\n')
            index = int(cmds[1:])

            #checks if the user-provided history index is valid, 
            # ensuring it's within the range of available commands 
            # in the command_history list. If valid, it retrieves 
            # and executes the command; otherwise, it returns an 
            # error indicating the index is out of range.
            if 1 <= index <= len(commands_history): 
                cmds_vlu = commands_history[index-1] # suppose user enter id = 16 but index in list is 15. 
                if cmds_vlu[1].strip() == "history":
                    return ""
                else:
                    return {"status_code": "200", "message": "", "data": cmds_vlu[1].strip()}
            else:
                raise Exception(f"index {index} out of range") 

        except Exception as e:
            return {"status_code": "404", "message": f"{e}", "data": []}

    else:
        return ""
    

