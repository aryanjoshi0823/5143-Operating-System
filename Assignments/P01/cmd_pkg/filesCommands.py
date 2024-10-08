
import os
import traceback
import sys
import shutil
from cmd_pkg.cmdsLogger import CmdsLogger
from cmd_pkg.getch import Getch
import traceback

getch = Getch()

# commmands to be executed 
# mv pm.txt bana
# cp /home/jarvis/Documents/others/test1.txt /home/jarvis/Documents/others/test_dir
# rm -rf bana
# cat write.txt
# less test.py
# head -n 10 abc.txt
# tail -n 10 abc.txt
# touch <filename>

def cat(**kwargs):

    cmds_logger = CmdsLogger()
    sys.stdout = cmds_logger

    try:
        try:
            if kwargs["input"] != "" and kwargs["params"] == []:
                filename = kwargs["input"].splitlines()[1]
                print(filename)
            elif kwargs["params"] != []:
                for filename in kwargs["params"]:
                    print("\r")
                    print('filename',filename)
                    with open (filename, "r") as file:
                        each_line = file.readline()[:] 

                        for items in each_line:
                            print(items, end="")
            else:
                 print(
                    f"\ncat: missing file operand.\nTry 'cat --help' for more information.")
                 
        except Exception as e:
            print(f"\n An error occurred: {e}")
    finally:
        sys.stdout = sys.__stdout__    

    captured_output = "".join(cmds_logger.log_content)
    return captured_output

def head(**kwargs):

    cmds_logger = CmdsLogger()
    sys.stdout = cmds_logger

    count = 0
    length = 0
    begin = 0

    try:
        try:
            # Determines the number of lines (length) to print and where to start 
            # reading files based on the presence or absence of flags and parameters.

            if kwargs["flags"] == "":
                length = 5  # no flags mentioned print first 5 line.
                count = 0
            elif kwargs["flags"] == "n" and len(kwargs["params"]) > 0:
                #If the flag is "n" and parameters are provided, 
                # it sets the number of lines based on the first
                #  parameter and skips it in further processing.

                length = int(kwargs["params"][0])  # get the flag value like -n 10  <--
                begin = 1  # to skip number of lines flag value like -n 10 while looping
            elif kwargs["flags"] == "n" and kwargs["params"] == []:
                raise Exception(f"head: invalid trailing option -- 1.\nTry 'head --help' for more information.")


            if kwargs["params"] != [] and kwargs["input"].strip() == "":
                # length of total number of item in params, but if flag not mentioned it is set to count  = 0, length = 5 previously, 
                count = len(kwargs["params"]) 
                for i in range(begin, count): # looping as many items as items in params, if flag is there begin = 1, else begin = 0, count = 0
                    filename = kwargs["params"][i].strip() #
                    if os.path.isfile(filename):
                        print("==> ",filename," <==")
                    with open(filename, 'r') as file:
                        lines = file.readlines()[:length]
                    # print lines to console
                    for line in lines:
                        print(line, end='')
                    print("\r")

            elif kwargs["input"] != "":
                filename = kwargs["input"].splitlines()[1]
                if os.path.isfile(filename):
                    print("==> ",filename," <==")                
                with open(filename, 'r') as file:
                    lines = file.readlines()[:length]
                    # print lines to console
                    for line in lines:
                        print(line, end='')
            else:
                print( f"\nhead: invalid trailing option -- 1.\n Try 'head --help' for more information.")
                 
        except FileNotFoundError:
            print(f"\nFile not found: {filename}")
            print(f"\rhead: cannot open '{filename}' for reading: No such file or directory")

        except Exception as e:
            print(f"\n An error occurred: {e}")
           
    finally:
        sys.stdout = sys.__stdout__    

    captured_output = "".join(cmds_logger.log_content)
    return captured_output

def tail(**kwargs):

    cmds_logger = CmdsLogger()
    sys.stdout = cmds_logger

    count = 0
    length = 0
    begin = 0

    try:
        try:
            # Determines the number of lines (length) to print and where to start 
            # reading files based on the presence or absence of flags and parameters.

            if kwargs["flags"] == "":
                length = 5  # no flags mentioned print first 5 line.
                count = 0
            elif kwargs["flags"] == "n" and len(kwargs["params"]) > 0:
                #If the flag is "n" and parameters are provided, 
                # it sets the number of lines based on the first
                #  parameter and skips it in further processing.

                length = int(kwargs["params"][0])  # get the flag value like -n 10  <--
                begin = 1  # to skip number of lines flag value like -n 10 while looping
            elif kwargs["flags"] == "n" and kwargs["params"] == []:
                raise Exception(f"tail: invalid trailing option -- 1.\nTry 'tail --help' for more information.")


            if kwargs["params"] != [] and kwargs["input"].strip() == "":
                # length of total number of item in params, but if flag not mentioned it is set to count  = 0, length = 5 previously, 
                count = len(kwargs["params"]) 
                for i in range(begin, count): # looping as many items as items in params, if flag is there  then begin = 1, else begin = 0, count = 0
                    filename = kwargs["params"][i].strip() 
                    if os.path.isfile(filename):
                        print("==> ",filename," <==")
                    with open(filename, 'r') as file:
                        lines = file.readlines()
                    total_lines_count = len(open(filename).readlines())
                    length = 2 if total_lines_count < 5 else length
                    for i in range(total_lines_count - length , total_lines_count):
                        print(lines[i], end='')
                    print("\r")

            elif kwargs["input"] != "":
                filename = kwargs["input"].splitlines()[1]
                if os.path.isfile(filename):
                    print("==> ",filename," <==")                
                with open(filename, 'r') as file:
                    lines = file.readlines()
                tot_lines = len(open(filename).readlines())
                length = 5 if kwargs["flags"] == "" else length
                for i in range(tot_lines - length , tot_lines):
                    print(lines[i], end='')
            else:
                print( f"\nhead: invalid trailing option -- 1.\n Try 'head --help' for more information.")
                 
        except FileNotFoundError:
            print(f"\nFile not found: {filename}")
            print(f"\rhead: cannot open '{filename}' for reading: No such file or directory")

        except Exception as e:
            print(f"\n An error occurred: {e}")
            print(traceback.format_exc()) 
    finally:
        sys.stdout = sys.__stdout__    

    captured_output = "".join(cmds_logger.log_content)
    return captured_output

def touch(**kwargs):
    cmds_logger = CmdsLogger()
    sys.stdout = cmds_logger

    try:
        if kwargs["params"] != []:
            try:
                for filename in kwargs["params"]:
                    if filename != "&&" and not os.path.isfile("filename"):
                        open(filename, 'w').close()
            except Exception as e:
                print(f"\nAn error occurred: {e}")

        elif kwargs["params"] == [] and kwargs["input"] != []:
            # block for handling input from other command when using pipe
            pass
    finally:
        sys.stdout = sys.__stdout__   # Restore the original stdout
    captured_output = "".join(cmds_logger.log_content)
    return captured_output

def less(**kwargs):

    try:
        if kwargs["params"] != []:
            filename = kwargs["params"][0]
            with open (filename, "r") as file:
                lines = file.readlines()
            temp_content = " "
            each_pg_size = 3 # displayed lines
            curr_line = 0
            print("\n")

            while True:
                # Display the current page of lines
                for i in range(curr_line, min(curr_line + each_pg_size, len(lines))):
                    print(lines[i], end="")


                # Asking the user to continue or quit
                user_input_value = input(
                    "Press 'q' to quit, 'n' for the next page: ")
                if user_input_value.lower() == "q":
                    break
                elif user_input_value.lower() == "n":
                    curr_line += each_pg_size
                    if curr_line >= len(lines):
                        break
        else:
            print(f"\nless: invalid trailing option -- 1.\nTry 'less --help' for more information.")
    except FileNotFoundError:
        print(f"\rless: cannot open '{filename}' for reading: No such file or directory")
    except Exception as e:
        print(f"\rAn error occurred: {e}.\nTry 'less --help' for more information.")

def mv(**kwargs):
    cmds_logger = CmdsLogger()
    sys.stdout = cmds_logger
    try:
        if kwargs["params"] != []:
            try:
                params_values  = kwargs["params"]
                count_params_value = len(params_values)

                if count_params_value == 1:
                    print(f"\ncp: missing file operand\nTry 'cp --help' for more information.")

                elif count_params_value == 2:
                    first_param = params_values[0]
                    second_param = params_values[1]

                    #shutil.move(file1, file2) moves a file or directory from file1 to file2.
                    #If file2 is a directory, file1 is moved into it.
                    #If file2 is a file, file1 replaces file2.
                    shutil.move(first_param, second_param)

                elif count_params_value > 1:
                    destination = params_values[-1]
                    if os.path.isdir(destination):
                        for filename in kwargs["params"][:-1]:
                            if os.path.isfile(filename):
                                shutil.move(filename, destination)
                            else:
                                raise Exception(f"mv: cannot stat '{filename}': No such file or directory")
                    else:
                        raise Exception(f"mv: target '{destination}' is not a directory")
                    
                elif kwargs["params"] == [] and kwargs["input"] != '':
                    # this block is used Incase an Input is received from a pipe
                    pass

            except FileNotFoundError:
                print(f"\nmv: cannot open '{second_param}' for reading: No such file or directory")

            except Exception as e:
                print(f"\n An error occurred: {e}")
                print(traceback.format_exc()) 
        else:
            print(f"\nmv: missing file operand\nTry 'mv --help' for more information.")

    finally:
        sys.stdout = sys.__stdout__    


    captured_output = "".join(cmds_logger.log_content)
    return captured_output

def cp(**kwargs):
    cmds_logger = CmdsLogger
    sys.stdout = cmds_logger

    try:
        if kwargs["params"] != []:
            try:
                params_value = kwargs["params"]
                count_params_value = len(kwargs["params"])

                if count_params_value == 1: 
                    print(f"\ncp: missing file operand\nTry 'cp --help' for more information.")

                elif count_params_value == 2:
                    first_params = params_value[0]
                    second_params = params_value[1]

                    shutil.copytree(first_params, second_params) if kwargs["flags"] in ('r','R') else shutil.copy(first_params, second_params)

                elif count_params_value > 2:
                    destination = params_value[-1]
                    if os.path.isdir(destination):
                        for filename in kwargs["params"][-1]:
                            if os.path.isfile(filename):
                                shutil.copy(filename, destination)
                            else:
                                raise Exception( f"cp: cannot stat '{filename}': No such file or directory")
                    else:
                        raise Exception(f"cp: cannot stat '{filename}': No such file or directory")
                    
                            
                elif kwargs["params"] == [] and kwargs["input"] != '':
                    # this block is used Incase an Input is received from a pipe
                    pass
            
            except FileNotFoundError:
                print(
                    f"\ncp: cannot open '{second_params}' for reading: No such file or directory")
                
            except Exception as e:
                print(f"An error occurred: {e}")

        else:
            print(f"\ncp: missing file operand\nTry 'cp --help' for more information.")


    finally:
       sys.stdout = sys. __stdout__

    captured_output = "".join(cmds_logger.log_content)
    return captured_output


def rm(**kwargs):
    try:
        if kwargs["params"] != []:
            try:
                for filename in kwargs["params"]:
                    # Check if it's a directory or a file
                    if os.path.isdir(filename):
                        # Use rmtree for directories
                        shutil.rmtree(filename) if kwargs["flags"] in ('r', 'R', 'rf', 'fr') else print(f"rm: cannot remove '{filename}': Is a directory")
                    elif os.path.isfile(filename):
                        # Use os.remove for files
                        os.remove(filename)
                    else:
                        print(f"rm: cannot remove '{filename}': No such file or directory")
            except Exception as e:
                print(f"An error occurred: {e}")
        elif kwargs["params"] == [] and kwargs["input"] != '':
            filename = kwargs["input"].splitlines()[1]
            os.remove(filename)
        else:
            print(f"\nrm: missing file operand.\nTry 'rm --help' for more information.")

    except FileNotFoundError:
        print(f"\rrm:'{filename}' No such file or directory")
    except Exception as e:
        print(f"\rAn error occurred: {e}.\nTry 'rm --help' for more information.")
