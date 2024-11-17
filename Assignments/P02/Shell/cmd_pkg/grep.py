from helper_files.api_call import *
from helper_files.utils import *
from helper_files.cmdsLogger import PrintCaptureLogger
import sys
from colorama import Fore


def grep(**kwargs):

    print_capture_logger = PrintCaptureLogger()
    sys.stdout = print_capture_logger

    try:
        config = load_config()
        try:
            input = kwargs["input"] if kwargs.get("input") else []
            params = kwargs["params"] if kwargs.get("params") else []
            flags = kwargs["flags"] if kwargs.get("flags") else []

            print('\n')

            if params:

                src_parameter = params[0].replace("'", "").replace('"', '')
                src_files_name = params[1:]

                if src_files_name and src_parameter:
                    for file in src_files_name:

                        rd = read_file_data(file, config['cwdid'])
                        if rd["status_code"] == '200' and rd["data"] is not None:
                            res_data = rd["data"].splitlines()

                            match_count = 0  # Counter for matching lines
                            unique_files = set()  # To track unique files if '-l' flag is used

                            for line in res_data:
                                line_to_check = line.strip()

                                # Case-insensitive search if 'i' flag is present
                                if 'i' in flags:
                                    if src_parameter.lower() in line_to_check.lower():
                                        match_count += 1
                                        if 'l' in flags:
                                            unique_files.add(file.split("/")[-1])
                                        elif 'c' not in flags:
                                            print(line_to_check)
                                else:
                                    if src_parameter in line_to_check:
                                        match_count += 1
                                        if 'l' in flags:
                                            unique_files.add(file.split("/")[-1])
                                        elif 'c' not in flags:
                                            print(line_to_check)
                            
                            # Print the count of matching lines if '-c' flag is present
                            if 'c' in flags:
                                if match_count > 0: 
                                    c_flag_vlu = f"{match_count} match count"
                                    print(c_flag_vlu)
                                
                            # Print unique file names for '-l' flag
                            if 'l' in flags:
                                for f in unique_files:
                                    print(f)
                        else:
                            raise Exception(f"{rd['message']}")

                # If no files are provided, process input text
                else:
                    lines = input.splitlines()
                    match_count = 0  # Counter for input text matches

                    for line in lines:
                        line_to_check = line.strip()

                        if 'i' in flags:
                            if src_parameter.lower() in line_to_check.lower():  # Case-insensitive check
                                match_count += 1
                                if 'c' not in flags:
                                    print(line_to_check.strip())
                        else:
                            if src_parameter in line_to_check:  # Case-sensitive check
                                match_count += 1
                                if 'c' not in flags:
                                    print(line_to_check.strip())

                    if 'c' in flags:
                        print(f"{match_count} match count")

            else:
                raise Exception("Search pattern or file name required")

        except Exception as e:
            print(Fore.RED+f"grep: {e}")
    finally:
        sys.stdout = sys.__stdout__  # Restore the original stdout

    captured_output = ''.join(print_capture_logger.log_content)
    return captured_output

