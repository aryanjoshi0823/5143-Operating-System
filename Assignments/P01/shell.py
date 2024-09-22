"""  
need to change -- >
---------------------:-
This file is about using getch to capture input and handle certain keys 
when the are pushed. The 'command_helper.py' was about parsing and calling functions.
This file is about capturing the user input so that you can mimic shell behavior.

"""

##################################################################################
##################################################################################

import os
import sys
import re
import importlib
import pkgutil
import cmd_pkg
from time import sleep

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


# Get the docstring of a function
# def get_docstring(func_name):
#     if func_name in cmds:
#         return cmds[func_name].__doc__
#     else:
#         return f"Function '{func_name}' not found."

def print_cmd(cmd):
    """This function "cleans" off the command line, then prints
    whatever cmd that is passed to it to the bottom of the terminal.
    """

    prompts= loaded_cmds.get('prompt') 
    prompt_vlu = prompts()
    padding = " " * 80
    sys.stdout.write("\r" + padding)
    sys.stdout.write("\r" + prompt_vlu + cmd)
    sys.stdout.flush()


if __name__ == "__main__":

    load_commands()

    Getch = loaded_cmds.get('Getch') 
    getch = Getch()
 
    input_cmd = ""
    print(input_cmd)

    index = 0
    history_list = []

    params = ["/usr/local/bin"]

  

    while True:  # loop forever

        char = getch() # read a character (but don't print) 

        if char == "\x03" or input_cmd == "exit":  # ctrl-c
            raise SystemExit("Bye.")

        elif char == "\x7f":  # back space pressed
            input_cmd = input_cmd[:-1]
            print_cmd(input_cmd)

        elif char in "\x1b":  # arrow key pressed
            null = getch()  # waste a character
            direction = getch()  # grab the direction

            if direction in "A":  # up arrow pressed
                # get the PREVIOUS command from your history (if there is one)
                # prints out 'up' then erases it (just to show something)
                input_cmd += "\u2191"
                print_cmd(input_cmd)
                sleep(0.3)
                # cmd = cmd[:-1]

            if direction in "B":  # down arrow pressed
                # get the NEXT command from history (if there is one)
                # prints out 'down' then erases it (just to show something)
                input_cmd += "\u2193"
                print_cmd(input_cmd)
                sleep(0.3)
                # cmd = cmd[:-1]

            if direction in "C":  # right arrow pressed
                # move the cursor to the right on your command prompt line
                # prints out 'right' then erases it (just to show something)
                input_cmd += "\u2192"
                print_cmd(input_cmd)
                sleep(0.3)
                # cmd = cmd[:-1]

            if direction in "D":  # left arrow pressed
                # moves the cursor to the left on your command prompt line
                # prints out 'left' then erases it (just to show something)
                input_cmd += "\u2190"
                print_cmd(input_cmd)
                sleep(0.3)
                # cmd = cmd[:-1]

            print_cmd(input_cmd)  # print the command (again)

        elif char in "\r":  # return pressed

            # This 'elif' simulates something "happening" after pressing return
            input_cmd = "Executing command...."  #
            print_cmd(input_cmd)
            sleep(1)

            ## YOUR CODE HERE
            ## Parse the command
            ## Figure out what your executing like finding pipes and redirects
            ## Call the function dynamically from the dictionary
            if input_cmd in loaded_cmds:
                result = loaded_cmds[input_cmd](params = params)
                print(result)
            else:
                print(f"Command '{input_cmd}' not found.")

            input_cmd = ""  # reset command to nothing (since we just executed it)

            print_cmd(input_cmd)  # now print empty cmd prompt
        else:
            input_cmd += char  # add typed character to our "cmd"
            print_cmd(input_cmd)  # print the cmd out








  