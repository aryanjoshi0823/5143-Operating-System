""" Methods written to implement the shell command 'History'. """

import os
import readline
from cmd_pkg.cmdsLogger import CmdsLogger
import sys

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
    cmds_logger = CmdsLogger()

    # Redirects sys.stdout to cmds_logger, so any printed 
    # output is captured by the cmds_logger instead of appearing in the console.
    sys.stdout = cmds_logger

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

        for index, item in enumerate(commands_history, start = 1):
            print(index, item)

    except Exception as e:
        print("An error occurred while displaying history:", e)

    finally:
        # remains unchanged regardless of how sys.stdout is manipulated,
        # ensuring you have a way to revert to the original output.
        sys.stdout = sys.__stdout__  # Restore the original stdout

        # concatenates all the strings stored in cmds_logger.log_content into a single string.
        captured_output = ''.join(cmds_logger.log_content)
        return captured_output
