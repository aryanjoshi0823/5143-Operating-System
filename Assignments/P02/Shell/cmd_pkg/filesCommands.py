import sys
import re
from helper_files.api_call import *
from helper_files.utils import *
from helper_files.cmdsLogger import PrintCaptureLogger
from colorama import Fore


def cat(**kwargs):
    print_capture_logger = PrintCaptureLogger()
    sys.stdout = print_capture_logger

    try:
        config = load_config()

        input = kwargs["input"] if kwargs.get("input") else []
        params = kwargs["params"] if kwargs.get("params") else []
        flags = kwargs["flags"] if kwargs.get("flags") else []

        try:
            if input and params == []:
                data = input.splitlines()
                print(data)

            elif params and input == []:

                cat_output = ""
                name = ""

                for param in params:
                    parts = param.split("/")[-1]
                    name = name + " "+ parts 

                    param = param.replace("'", "").replace('"', "")
                    rd = read_file_data(param,config['cwdid'])

                    if rd["status_code"] == '200' and rd["data"] is not None:
                        cat_output += rd["data"]
                    else:
                        raise Exception(f"{rd["message"]}")

                print("filename",name)
                print(cat_output)
            else:
                raise Exception("cat: missing file operand.\nTry 'cat --help' for more information.")
                    
        except Exception as e:
            print(Fore.RED+f"\ncat: {e}")

    finally:
        sys.stdout = sys.__stdout__  # Restore the original stdout

    captured_output = ''.join(print_capture_logger.log_content)
    return captured_output

def head(**kwargs):
    print_capture_logger = PrintCaptureLogger()
    sys.stdout = print_capture_logger

    try:
        config = load_config()

        input = kwargs["input"] if kwargs.get("input") else []
        params = kwargs["params"] if kwargs.get("params") else []
        flags = kwargs["flags"] if kwargs.get("flags") else []

        count = 0
        length = 0
        begin = 0

        try:
            # Determines the number of lines (length) to print and where to start 
            # reading files based on the presence or absence of flags and parameters.

            if flags == []:
                length = 10  # no flags mentioned print first 10 line.
                count = 0

            elif flags[0] == "n" and len(params) > 0:
                #If the flag is "n" and parameters are provided, 
                # it sets the number of lines based on the first
                #  parameter and skips it in further processing.
                length = int(params[0]) # get the flag value like -n 10
                begin = 1 

            elif flags[0] == "n" and params == []:
                raise Exception("Try 'man head' for more information.")

            if params and input == []:
                count = len(params) 

                # looping as many items as items in params, if flag is [10, xyz, qwe] 
                # there begin = 1 to count ,  else begin = 0
                for i in range(begin, count):

                    filename = params[i].strip() 
                    rfd = read_file_data(params[i],config['cwdid'])

                    if rfd["status_code"] == '200' and rfd["data"] is not None:
                        file_parts = filename.split("/")
                        file_name = file_parts[-1]

                        print("==> ",file_name," <==")

                        data = rfd["data"].splitlines()
                        for line in data[:length]:
                            print(line)
                    else:
                        raise Exception(rfd["message"])
            
            elif input and params == []:
                filename = input.splitlines()
                for line in filename[:length]:
                    print(line)

        except Exception as e:
            print(Fore.RED+f"\n head: {e}")

    finally:
        sys.stdout = sys.__stdout__  # Restore the original stdout

    captured_output = ''.join(print_capture_logger.log_content)
    return captured_output
           
def tail(**kwargs):
    print_capture_logger = PrintCaptureLogger()
    sys.stdout = print_capture_logger

    try:
        config = load_config()

        input = kwargs["input"] if kwargs.get("input") else []
        params = kwargs["params"] if kwargs.get("params") else []
        flags = kwargs["flags"] if kwargs.get("flags") else []

        count = 0
        length = 0
        begin = 0

        try:
            # Determines the number of lines (length) to print and where to start 
            # reading files based on the presence or absence of flags and parameters.

            if flags == []:
                length = 10  
                count = 0

            elif flags[0] == "n" and len(params) > 0:

                #If the flag is "n" and parameters are provided, 
                # it sets the number of lines based on the first
                #  parameter and skips it in further processing.

                length = int(params[0])  
                begin = 1  

            elif flags[0] == "n" and params == []:
                raise Exception(f"invalid trailing option -- 1.\nTry 'man tail' for more information.")

            if params and input == []:

                count = len(params) 
                for i in range(begin, count): 

                    filename = params[i].strip() 
                    rfd = read_file_data(params[i],config['cwdid'])

                    if rfd["status_code"] == '200' and rfd["data"] is not None:
                        file_parts = filename.split("/")
                        file_name = file_parts[-1]

                        print("==> ",file_name," <==")

                        data = rfd["data"].splitlines()
                        total_lines_count = len(data)

                        length = 2 if total_lines_count < 5 else length
                        for i in range(total_lines_count - length, total_lines_count):
                            print(data[i])
                    else:
                        raise Exception(rfd["message"])

            elif input:
                filename = input.splitlines()
                total_lines_count = len(filename)
                length = 2 if total_lines_count < 5 else length
                for i in range(total_lines_count - length, total_lines_count):
                    print(filename[i])

            else:
                raise Exception( f"parameter is needed.")

        except Exception as e:
            print(Fore.RED+f"\n tail: {e}")

    finally:
        sys.stdout = sys.__stdout__  # Restore the original stdout

    captured_output = ''.join(print_capture_logger.log_content)
    return captured_output
 
def touch(**kwargs):
    print_capture_logger = PrintCaptureLogger()
    sys.stdout = print_capture_logger

    try:
        input = kwargs["input"] if kwargs.get("input") else []
        params = kwargs["params"] if kwargs.get("params") else []
        flags = kwargs["flags"] if kwargs.get("flags") else []

        try:
            config = load_config()
            if params and input == [] and flags == []:
                try:
                    for param in params:
                        param = param.replace("'", "").replace('"', "")
                        mk_file_res = make_file(param,config['cwdid'])
                        if mk_file_res["status_code"] == '200' and mk_file_res["data"] is not None:
                            pass
                        else:
                            raise Exception(f"{mk_file_res["message"]}")
                except Exception as e:
                    raise Exception(f"{e}")

            elif params == [] and input:
                # block for handling input from other command when using pipe
                pass

        except Exception as e:
            print(Fore.RED+f"\n touch: {e}")
        
    finally:
        sys.stdout = sys.__stdout__  # Restore the original stdout

    captured_output = ''.join(print_capture_logger.log_content)
    return captured_output

def less(**kwargs):
    config = load_config()

    params = kwargs["params"] if kwargs.get("params") else []
    inputs = kwargs["input"] if kwargs.get("input") else []
    flags = kwargs["flags"] if kwargs.get("flags") else []

    try:
        line = ""
        if params:
            filename = params[0]
            filename = filename.replace("'", "").replace('"', "")

            rd = read_file_data(filename, config['cwdid'])
            if rd["status_code"] == '200' and rd["data"] is not None:
                lines = rd["data"].splitlines()
        elif inputs:
            lines = inputs.splitlines()
        else:
            raise Exception(f"\nTry 'man less' for more information.")

        each_pg_size = 20
        curr_line = 0
        search_vlu = None

        print("\n")

        while True:
            print("\033[H\033[J", end="")
            for i in range(curr_line, min(curr_line + each_pg_size, len(lines))):
                print(lines[i], end="\n")
                line = lines[i]

                # If there is a search term, highlight the matching term in the line
                if search_vlu:
                    line = re.sub(f"({re.escape(search_vlu)})", r'\033[1;31m\1\033[0m', line, flags=re.IGNORECASE)

                print(line, end="\n")


            user_input_value = input(
                "\n Press 'q' to quit, \n'n' for the next page, \n'b' for previous page: \n's' to search \n")
            if user_input_value.lower() == "q":
                break

            elif user_input_value.lower() == "n":
                curr_line += each_pg_size
                if curr_line >= len(lines):
                    print("\nEnd of content.")
                    break

            elif user_input_value.lower() == "b":
                curr_line -= each_pg_size
                if curr_line < 0:
                    print("\nEnd of content.")
                    break

            elif user_input_value.lower() == "s":
                search_vlu = input("Enter search term: ")
                search_vlu = search_vlu.strip()  # Strip any extra spaces
                if not search_vlu:
                    print("Invalid search term. Please try again.")
                else:
                    print(f"Searching for: {search_vlu}")
        return ''
    except Exception as e:
        print(Fore.RED+f"\n less: {e}")

def mv(**kwargs):
    print_capture_logger = PrintCaptureLogger()
    sys.stdout = print_capture_logger

    try:
        input = kwargs["input"] if kwargs.get("input") else []
        params = kwargs["params"] if kwargs.get("params") else []
        flags = kwargs["flags"] if kwargs.get("flags") else []

        try:
            config = load_config()

            if params and input == [] and flags == []:
                rfd = mv_file(params[0].strip(),params[1].strip(),config['cwdid'])
                if rfd["status_code"] == '200' and rfd["data"] is not None:
                    pass

                elif rfd["status_code"] == '404' and rfd["data"] == "dError":
                    rename = rename_file(params[0].strip(),params[1].strip(),config['cwdid'])
                    if rename["status_code"] == '200' and rename["data"] is not None:
                        pass
                else:
                    raise Exception(f"{rfd["message"]}")
                        
            elif input and flags:
                pass
        except Exception as e:
            print(Fore.RED+f"\n mv: {e}")
        
    finally:
        sys.stdout = sys.__stdout__  

    captured_output = ''.join(print_capture_logger.log_content)
    return captured_output

def cp(**kwargs):

    print_capture_logger = PrintCaptureLogger()
    sys.stdout = print_capture_logger

    try:
        input = kwargs["input"] if kwargs.get("input") else []
        params = kwargs["params"] if kwargs.get("params") else []
        flags = kwargs["flags"] if kwargs.get("flags") else []

        config = load_config()

        try:
            if params: 
                rfd = copy_file(params[0].strip(),params[1].strip(),config['cwdid'])
                if rfd["status_code"] == '200' and rfd["data"] is not None:
                    pass
                else:
                    print(rfd["message"] ) 
                
        except Exception as e:
            print(Fore.RED+f"cp: {e}")
    finally:
        sys.stdout = sys.__stdout__  # Restore the original stdout

    captured_output = ''.join(print_capture_logger.log_content)
    return captured_output

def rm(**kwargs):
    print_capture_logger = PrintCaptureLogger()
    sys.stdout = print_capture_logger

    try:
        input = kwargs["input"] if kwargs.get("input") else []
        params = kwargs["params"] if kwargs.get("params") else []
        flags = kwargs["flags"] if kwargs.get("flags") else []

        config = load_config()

        try:
            if params:

                rfd = delete_file(params[0].strip(),config['cwdid'])
                if rfd["status_code"] == '200' and rfd["data"] is not None:
                    pass
                else:
                    print(rfd["message"] )  
                
        except Exception as e:
            print(Fore.RED+f"rm: {e}")
    finally:
        sys.stdout = sys.__stdout__  # Restore the original stdout

    captured_output = ''.join(print_capture_logger.log_content)
    return captured_output