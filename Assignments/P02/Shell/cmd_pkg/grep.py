from helper_files.api_call import *
from helper_files.utils import *

def grep(**kwargs):
    config = load_config()
    try:
        input = kwargs["input"] if kwargs.get("input") else []
        params = kwargs["params"] if kwargs.get("params") else []
        flags = kwargs["flags"] if kwargs.get("flags") else []

        print('\n')

        if params:

            src_parameter = params[0].replace("'", "").replace('"', '')
            src_files_name = params[1:]

            unique_files = set()  # To track unique files if '-l' flag is used

            if src_files_name:
                for file in src_files_name:

                    rd = read_file_data(file, config['cwdid'])
                    if rd["status_code"] == '200' and rd["data"] is not None:
                        res_data = rd["data"].splitlines()

                        match_count = 0  # Counter for matching lines

                        line_to_check_vlu = ""
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
                                        line_to_check_vlu = line_to_check_vlu + "\n" + line_to_check
                            else:
                                if src_parameter in line_to_check:
                                    match_count += 1
                                    if 'l' in flags:
                                        unique_files.add(file.split("/")[-1])
                                    elif 'c' not in flags:
                                        print(line_to_check)
                                        line_to_check_vlu = line_to_check_vlu + "\n" + line_to_check
                        
                        # Print the count of matching lines if '-c' flag is present
                        if 'c' in flags:
                            c_flag_vlu = f"{match_count} {file.split('/')[-1]}"
                            print(c_flag_vlu)
                            return(str(c_flag_vlu))
                            

                        # Print unique file names for '-l' flag
                        if 'l' in flags:
                            for f in unique_files:
                                print(f)
                            return(str(unique_files))
                        
                        return(str(line_to_check_vlu))

                    else:
                        print(f"{rd['message']}")

            # If no files are provided, process input text
            else:
                lines = input.split("\n")
                match_count = 0  # Counter for input text matches

                line_to_check_input = ""
                if 'l' in flags and len(lines) > 1:
                    for each_line in lines:
                        if src_parameter.lower() in each_line.lower():
                            temp = each_line
                            line_to_check_input= line_to_check_input + "\n" + temp
                            print('t--',temp)

                for line in lines:
                    if 'i' in flags:
                        if src_parameter.lower() in line.lower():  # Case-insensitive check
                            match_count += 1
                            if 'c' not in flags:
                                line_to_check_input= line_to_check_input + "\n" + line.strip()
                                print(line.strip())
                    else:
                        if src_parameter in line:  # Case-sensitive check
                            match_count += 1
                            if 'c' not in flags:
                                line_to_check_input= line_to_check_input + "\n" + line.strip()
                                print(line.strip())

                if 'c' in flags:
                    x= f"{match_count} match count"
                    print(f"{match_count} match count")
                    return(str(x))
                return(str(line_to_check_input))

        else:
            print("Search pattern or file name required")

    except Exception as e:
        print(f"\rAn error occurred: {e}.")

