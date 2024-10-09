
import os
import pwd
import grp
import time
import stat
import logging
import sys
from cmd_pkg.cmdsLogger import CmdsLogger

def grep(**kwargs):

    cmds_logger = CmdsLogger()
    sys.stdout = cmds_logger

    try:

        input = kwargs["input"] if kwargs.get("input") else []
        params = kwargs["params"] if kwargs.get("params") else []
        flags = kwargs["flags"] if kwargs.get("flags") else []

        print('\n')

        if params:
            #first parameter consider search pattern and any quote is removed.
            src_parameter = params[0].replace("'", "").replace('"', '')
            
            # rest of the value from params
            src_files_name = params[1:]

            #A set named unique_files is created to keep track of files that
            # match the search pattern if the -l flag is specified.
            unique_files = set()

            if src_files_name:
                for file in src_files_name:
                    with open(file,'r') as f:
                        for line in f:
                            line_to_check = line.strip() 

                            # if i flag present then ignore the case.
                            if 'i' in flags:
                                if src_parameter.lower() in line_to_check.lower():
                                    if "l" in flags:
                                        unique_files.add(f.name) # name of the file currently opened by with open()
                                    else:
                                        print(line_to_check)

                            else:
                                if src_parameter in line_to_check:
                                    if "l" in flags:
                                        unique_files.add(f.name) 
                                    else:
                                        print(line_to_check)

                        # printing unique_files content.         
                        if "l" in flags:
                            for f in unique_files:
                                print(f)
                            
            # If no files are provided, process input text
            else:
                lines = input.split("\n")
                if "l" in flags and len(lines) > 1:
                    print("(standard input)")

                for line in lines:
                    if "i" in flags:
                        if src_parameter.lower() in line.lower():  # Case-insensitive check
                            print(line.strip())
                    else:
                        if src_parameter in line:  # Case-sensitive check
                            print(line.strip())
                
        else:
            print("Search pattern or file name required")

    except FileNotFoundError:
        print(f"\rless: cannot open '{file}' for reading: No such file or directory")
    except Exception as e:
        print(f"\rAn error occurred: {e}.\nTry 'less --help' for more information.")

    finally:
        sys.stdout = sys.__stdout__

    captured_output = ''.join(cmds_logger.log_content)
    return captured_output
