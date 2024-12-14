import os
import sys
import shlex
import importlib
import pkgutil
import cmd_pkg
from time import sleep
import json
from colorama import Fore, Style
from cmd_pkg.history import commands_history
from helper_files.api_call import *



def load_config(file_path=".config"):
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config

config = load_config()
loaded_cmds = {}

history_list = commands_history
length =len(commands_history)-1
cmd_list_index = length

# Dynamically load all functions from cmd_pkg into the dictionary cmd
def load_commands():
    global loaded_cmds

    # Loop through all modules in the cmd_pkg package
    for _, module_name, _ in pkgutil.iter_modules(cmd_pkg.__path__):
        module = importlib.import_module(f"cmd_pkg.{module_name}")

        # Loop through the attributes in each module
        for name in dir(module):
            obj = getattr(module, name)
            # Check if it's a callable function and doesn't start with '__'
            if callable(obj) and not name.startswith("__"):
                loaded_cmds[name] = obj
    
def print_cmd(cmd, config, cursor_pos = 0):
    """This function "cleans" off the command line, then prints
    whatever cmd that is passed to it to the bottom of the terminal.
    """
    padding = " " * 80
    current_user = config['user']
    root_or_home = config['root_or_home']
    cwd = config['cwd']

    prompt = (
        Fore.GREEN + current_user + " " +               
        Fore.YELLOW + root_or_home + " " +             
        Fore.BLUE + cwd +                              
        Fore.WHITE + " $" +                       
        Style.RESET_ALL                             
    )

    sys.stdout.write("\r" + padding)
    sys.stdout.write("\r" + prompt + cmd)
    sys.stdout.flush()

    #Position cursor after printed command
    cursor_move_back = len(cmd) - cursor_pos
    if cursor_move_back > 0:
        sys.stdout.write(f"\033[{cursor_move_back}D")
    sys.stdout.flush()

if __name__ == "__main__":

    load_commands()

    Getch = loaded_cmds.get('Getch') 
    getch = Getch()
 
    input_cmd = ""
    cursor_pos = 0
    print_cmd(input_cmd, config, cursor_pos)

    while True: 

        char = getch() # read a character (but don't print) 

        if char == "\x03" or input_cmd == "exit":  # ctrl-c
            raise SystemExit("")

        elif char == "\x7f":  # back space pressed
            if cursor_pos > 0:
                # Remove the character at the cursor position and adjust the cursor position
                input_cmd = input_cmd[:cursor_pos-1] + input_cmd[cursor_pos:]
                cursor_pos -= 1
                print("\b \b", end='')  # Move cursor back and erase the character
                print_cmd(input_cmd, config, cursor_pos)

        #\x1b is the escape character in Python (hex 0x1b), 
        # corresponding to the ASCII "escape" (ESC). It's
        #  used in sequences for special keys like arrow 
        # keys and function keys.
        elif char in "\x1b": 
            null = getch()  # waste a character
            direction = getch()  # grab the direction

            if direction in "A":  # up arrow 
                # get the PREVIOUS command from your history (if there is one)
                if history_list == []:
                    pass
                elif cmd_list_index > 0:
                    input_cmd = history_list[cmd_list_index][1]
                    cursor_pos = (len(input_cmd))
                    print_cmd(history_list[cmd_list_index][1],config,cursor_pos)
                    cmd_list_index -= 1

                elif cmd_list_index == 0:
                    input_cmd = history_list[0][1]
                    cursor_pos = (len(input_cmd))
                    print_cmd(history_list[0][1],config,cursor_pos)
                sleep(0.1)


            if direction in "B":  # down arrow 
                # get the NEXT command from history (if there is one)
                if history_list == []:
                    pass
                elif cmd_list_index < length:
                    input_cmd = history_list[cmd_list_index][1]
                    cursor_pos = (len(input_cmd))
                    print_cmd(history_list[cmd_list_index][1],config,cursor_pos)
                    cmd_list_index += 1

                elif cmd_list_index == length:
                    input_cmd = history_list[cmd_list_index][1]
                    cursor_pos = (len(input_cmd))
                    print_cmd(history_list[cmd_list_index][1],config,cursor_pos)
                sleep(0.1)

            if direction in "C":  # right arrow 
                if cursor_pos < len(input_cmd):
                    cursor_pos += 1
                    sys.stdout.write("\033[C")  # Move the cursor right by one position
                    sys.stdout.flush()

            if direction in "D":  # left arrow pressed
                if cursor_pos > 0:
                    cursor_pos -= 1
                    sys.stdout.write("\033[D")  # Move the cursor left by one position
                    sys.stdout.flush()
                    
        elif char in "\r":  # enter pressed

            try:
                left_cmds, redirect_cmd  = input_cmd.split('>',1) if '>' in input_cmd else (input_cmd, '')
                left_cmds_pipe = left_cmds.split('|')
                captured_output = ""

                # The line checks if there are multiple piped commands and if the 
                # first command is "ls". If true, it sets captured_output to "ls" 
                # for special handling.

                if len(left_cmds_pipe) > 0 and left_cmds_pipe[0].split()[0].strip() == "ls":
                    captured_output = "ls"

                for each_commands in left_cmds_pipe:

                    parts = []

                    # for !x
                    if each_commands.strip().startswith('!'):
                        cmds_from_history_vlu= loaded_cmds.get('cmds_from_history') 
                        cmd_x = cmds_from_history_vlu(each_commands.strip())

                        if cmd_x["status_code"]=="200":
                            print(cmd_x)
                            if cmd_x and cmd_x["data"].strip().split()[0] == "ls":
                                captured_output = "ls"

                            each_commands = cmd_x["data"]
                        else:
                            raise Exception(cmd_x["message"]) 
                            
                    parts = shlex.split(each_commands)

                    #first part of the command like 'ls'.
                    first_part = parts[0].strip() if parts else ""

                    # other parameters
                    params = []
                    flags = []

                    # parse flags, params, help 
                    for each_part in parts[1:]:
                        if each_part.startswith('-'):
                            if each_part.startswith('--'):
                                raise Exception(f"'{each_part}' not found.") 
                            else:
                                flags.append(each_part.lstrip('-').strip())
                        else:
                            params.append(each_part.strip())
                    
                    # Invoke the command if it exists in the dynamically loaded commands
                    if first_part in loaded_cmds:
                        try:
                            # retrieves the function associated 
                            command_func = loaded_cmds[first_part]   
                            captured_output = command_func(params=params, flags=' '.join(flags), input=captured_output)
                                
                        except Exception as e:
                            print(Fore.RED+f"\n{first_part}: {str(e)}")
                    else:
                        raise Exception(f"Command '{first_part}' not found.")

                    #adding to history, in return getting length, command history list
                    add_cmd_to_history = loaded_cmds.get('add_commands')
                    history_list, length = add_cmd_to_history(each_commands,flags)
                    cmd_list_index = length

                if redirect_cmd:
                    redirected_file = redirect_cmd.strip()
                    temp = write_file(redirected_file, config['cwdid'], captured_output)
                    print(Fore.GREEN + f"\n{temp["message"]}")
                else:
                    print("\n")
                    print( Fore.GREEN + f"{captured_output}")
  
            except Exception as e:
                print(Fore.RED+f"\n Error: {e}\n")

            config = load_config()     
            input_cmd = "" 
            cursor_pos = 0
            print_cmd(input_cmd,config,cursor_pos) 

        else:
            input_cmd = input_cmd[:cursor_pos] + char + input_cmd[cursor_pos:]
            cursor_pos += 1  # Move cursor right after adding character
            print_cmd(input_cmd, config, cursor_pos)


