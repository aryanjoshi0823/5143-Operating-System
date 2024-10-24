import os
import sys
import shlex
import importlib
import pkgutil
import cmd_pkg
from time import sleep
import json
from colorama import Fore, Style


def load_config(file_path=".config"):
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config

# Load the config
config = load_config()

# Dictionary to store the commands from cmd_pkg.
loaded_cmds = {}
command_history=[]


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
    
def print_cmd(cmd, config):
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



if __name__ == "__main__":

    load_commands()

    Getch = loaded_cmds.get('Getch') 
    getch = Getch()
 
    input_cmd = ""
    print(input_cmd)

    index = 0
    history_list = []

    while True:  # loop forever

        char = getch() # read a character (but don't print) 

        if char == "\x03" or input_cmd == "exit":  # ctrl-c
            raise SystemExit("")

        elif char == "\x7f":  # back space pressed
            input_cmd = input_cmd[:-1]
            
            # Move the cursor back and erase the character, end='' prevent print 
            # function to add newline so the cursor stays on the same line after printing.
            print("\b \b", end='') 
            print_cmd(input_cmd,config)

        #\x1b is the escape character in Python (hex 0x1b), 
        # corresponding to the ASCII "escape" (ESC). It's
        #  used in sequences for special keys like arrow 
        # keys and function keys.
        elif char in "\x1b": 
            null = getch()  # waste a character
            direction = getch()  # grab the direction

            if direction in "A":  # up arrow pressed
                # get the PREVIOUS command from your history (if there is one)
                if history_list == []:
                    print_cmd("")
                elif index > 0:
                    print_cmd(history_list[index],config)
                    index -= 1
                elif index == 0:  
                    print_cmd(history_list[0],config)

                print_cmd(input_cmd,config)
                sleep(0.1)


            if direction in "B":  # down arrow pressed
                # get the NEXT command from history (if there is one)
                if history_list == []:
                    print_cmd("")
                elif index < history_length:
                    print_cmd(history_list[index],config)
                    index += 1
                elif index == history_length:
                    print_cmd(history_list[index],config)
                sleep(0.1)

            if direction in "C":  # right arrow pressed
                sys.stdout.write("\033[C")  # Move the cursor right by one position
                sys.stdout.flush()

            if direction in "D":  # left arrow pressed
                sys.stdout.write("\033[D")  # Move the cursor left by one position
                sys.stdout.flush()
                    
        elif char in "\r":  # enter pressed

            left_cmds, redirect_cmd  = input_cmd.split('>',1) if '>' in input_cmd else (input_cmd, '')

            print("left_cmds-->",left_cmds)
            print("redirect_cmd-->",redirect_cmd)

            left_cmds_pipe = left_cmds.split('|')

            print("left_cmds_pipe-->",left_cmds_pipe)

            captured_output = ""

            # The line checks if there are multiple piped commands and if the 
            # first command is "ls". If true, it sets captured_output to "ls" 
            # for special handling.

            if len(left_cmds_pipe) > 0 and left_cmds_pipe[0].split()[0].strip() == "ls":
                captured_output = "ls"

            for each_commands in left_cmds_pipe:
                parts = shlex.split(each_commands)
                print("parts--->",parts)

                #first part of the command itself.
                first_part = parts[0].strip() if parts else ""
                print("first parts--->",first_part)

                # other parameters
                params = []
                flags = []
                helps = []

                # parse flags, params, help 
                for each_part in parts[1:]:
                    if each_part.startswith('-'):
                        if each_part.startswith('--'):
                            helps.append(each_part.lstrip('-').strip())
                        else:
                            flags.append(each_part.lstrip('-').strip())
                    else:
                        params.append(each_part.strip())
                
                print("params--->",params)
                print("flags--->",flags)
                print("helps--->",helps)
                print("captured_output in shell.py-->", captured_output)

                # Invoke the command if it exists in the dynamically loaded commands
                if first_part in loaded_cmds:
                    try:
                        # retrieves the function associated 
                        command_func = loaded_cmds[first_part]   
                        if helps:
                            captured_output = command_func(params=params, flags=' '.join(flags), help=' '.join(helps), input=captured_output)
                            #print("help cap output--->",captured_output)
                        else:
                            captured_output = command_func(params=params, flags=' '.join(flags), input=captured_output)
                            #print("no help cap output--->",captured_output)
                            
                    except Exception as e:
                        print(f"Error executing command {first_part}: {str(e)}")
                else:
                    # for !x
                    cmds_from_history_vlu= loaded_cmds.get('cmds_from_history') 
                    print("\r")
                    cmds_from_history_vlu(input_cmd)
                    if not input_cmd.startswith('!'):  
                        print(f"\nCommand '{first_part}' not found.")

                #adding to history
                add_to_history_fuc = loaded_cmds["add_commands_to_history"]
                (history_list,history_length) = add_to_history_fuc(each_commands, flags)
                index = history_length



            # Redirection
            if redirect_cmd:
                #save_output_to_file(captured_output,redirect_cmd)  
                pass
            else:
                print("\r")
                #print("--->",captured_output)
                  

            config = load_config()  
            #sleep(1)    
            input_cmd = "" 
            print_cmd(input_cmd,config) 


        elif char == ':':
            pass

        else:
            input_cmd += char  # add typed character to our "cmd"
            print_cmd(input_cmd,config)  
