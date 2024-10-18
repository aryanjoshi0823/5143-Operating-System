import os
from cmd_pkg.history import add_commands_to_history, history, commands_history

def execute_cmds(cmds):
    "Execute given commands and return the output"
    try:
        # Use os.system to run the command and redirect output to /dev/null (Unix) or nul (Windows)
        if os.name == "nt": 
            os.system(f"{cmds} > null")
        elif  os.name == "posix":# Windows system
            os.system(f"{cmds} > null")

        # commands output is redirected, return an empty string.    
        return ""
    except Exception as e:
        return f"Error: {str(e)}"


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
                cmds_vlu = commands_history[index-1]
                if cmds_vlu.strip() == "history":
                    return ""
                else:
                    os.system(cmds_vlu)
                    return ""
            else:
                return f"Error: Command history index {index} out of range."    
        except:
            return "Error: invalid history index"
    else:
        return ""
