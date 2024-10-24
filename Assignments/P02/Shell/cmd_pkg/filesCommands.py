from helper_files.api_call import *
from helper_files.utils import *

def cat(**kwargs):
    #/python_code/MyRTree/RTree2.py
    #state-fips.csv
    config = load_config()

    input = kwargs["input"] if kwargs.get("input") else []
    params = kwargs["params"] if kwargs.get("params") else []
    flags = kwargs["flags"] if kwargs.get("flags") else []
    
    try:
        if input:
            filename = input.splitlines()[1]
            print(filename)
            return(str(filename))

        elif params:

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
                    print(f"{rd["message"]}")

            print("filename",name)
            print(cat_output)
            return(str(cat_output))

        else:
            print(
            f"\ncat: missing file operand.\nTry 'cat --help' for more information.")
                
    except Exception as e:
        print(f"\n An error occurred: {e}")

def head(**kwargs):
    #/python_code/MyRTree/RTree2.py
    #state-fips.csv
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
            raise Exception(f"Try 'head --help' for more information.")

        if params and input == []:
            # count  = 0, length = 10 if flag = "", 
            count = len(params) 

            # looping as many items as items in params, if flag is [10, xyz, qwe] 
            # there begin = 1 to count ,  else begin = 0
            vlu_str = ""
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
                        vlu_str = vlu_str+"\n"+line
                else:
                    print(rfd["message"])
            return(str(vlu_str))
        
        elif input:

            filename = input.splitlines()[1]
            value = ""
            for line in filename[:length]:
                value = value+"\n"+line
                print(line)
            return(str(value))



                
    except Exception as e:
        print(f"\n An error occurred: {e}")
           
def tail(**kwargs):
    #/python_code/MyRTree/RTree2.py
    #state-fips.csv
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
            raise Exception(f"tail: invalid trailing option -- 1.\nTry 'tail --help' for more information.")

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
                    print(total_lines_count)

                    length = 2 if total_lines_count < 5 else length
                    for i in range(total_lines_count - length, total_lines_count):
                        print(data[i])
                else:
                    print(rfd["message"])

        elif input:

            filename = input.splitlines()[1]
            value = ""

            for line in filename[:length]:
                pass
            total_lines_count = len(filename)

            length = 2 if total_lines_count < 5 else length
            for i in range(total_lines_count - length, total_lines_count):
                value = value+"\n"+line
                print(data[i])
                
            return(str(value))

        else:
            print( f"\n tail: parameter is needed.")

    except Exception as e:
        print(f"\n An error occurred: {e}")
 
def touch(**kwargs):
        input = kwargs["input"] if kwargs.get("input") else []
        params = kwargs["params"] if kwargs.get("params") else []
        flags = kwargs["flags"] if kwargs.get("flags") else []

        config = load_config()
        if params:
            try:
                for param in params:
                    param = param.replace("'", "").replace('"', "")
                    mk_file_res = make_file(param,config['cwdid'])
                    if mk_file_res["status_code"] == '200' and mk_file_res["data"] is not None:
                        print("Files Created.")
                    else:
                        print(f"{mk_file_res["message"]}")
            except Exception as e:
                print(f"\n Error: {e}")

        elif params == [] and input:
            # block for handling input from other command when using pipe
            pass

def less(**kwargs):
     #/python_code/MyRTree/RTree2.py
    #state-fips.csv

    config = load_config()
    params = kwargs["params"] if kwargs.get("params") else []
    try:
        if params:
            filename = params[0]
            filename = filename.replace("'", "").replace('"', "")

            rd = read_file_data(filename, config['cwdid'])

            if rd["status_code"] == '200' and rd["data"] is not None:

                lines = rd["data"].splitlines()
                each_pg_size = 10
                curr_line = 0

                print("\n")

                while True:
                    # Display the current page of lines
                    for i in range(curr_line, min(curr_line + each_pg_size, len(lines))):
                        print(lines[i], end="\n")


                    # Asking the user to continue or quit
                    user_input_value = input(
                        "\n Press 'q' to quit, 'n' for the next page: ")
                    if user_input_value.lower() == "q":
                        break
                    elif user_input_value.lower() == "n":
                        curr_line += each_pg_size
                        if curr_line >= len(lines):
                            print("\nEnd of content.")
                            break
            else:
                print(f"{rd["message"]}")
        else:
            print(f"\nless: --help' for more information.")
    except Exception as e:
        print(f"\rAn error occurred: {e}.\nTry 'less --help' for more information.")

def mv(**kwargs):
    input = kwargs["input"] if kwargs.get("input") else []
    params = kwargs["params"] if kwargs.get("params") else []
    flags = kwargs["flags"] if kwargs.get("flags") else []

    print("params-->",params)
    config = load_config()

    rfd = mv_file(params[0].strip(),params[1].strip(),config['cwdid'])
    print("rfd--->",rfd)
    if rfd["status_code"] == '200' and rfd["data"] is not None:
        print("File moved.")

    elif rfd["status_code"] == '404':
        rename = rename_file(params[0].strip(),params[1].strip(),config['cwdid'])
        print("rename-->",rename)
        print(rename["message"]) 
        if rename["status_code"] == '200' and rename["data"] is not None:
            print("File renamed.")                       

def cp(**kwargs):

    input = kwargs["input"] if kwargs.get("input") else []
    params = kwargs["params"] if kwargs.get("params") else []
    flags = kwargs["flags"] if kwargs.get("flags") else []

    config = load_config()

    try:
        rfd = copy_file(params[0].strip(),params[1].strip(),params[2].strip(),config['cwdid'])
        if rfd["status_code"] == '200' and rfd["data"] is not None:
            print("File copied.")
        else:
            print(rfd["message"] ) 
                            
    except Exception as e:
        print(f"An error occurred: {e}")

#cp python_code/shapes.py python_code/testmode tshapes.py

def rm(**kwargs):
    input = kwargs["input"] if kwargs.get("input") else []
    params = kwargs["params"] if kwargs.get("params") else []
    flags = kwargs["flags"] if kwargs.get("flags") else []

    config = load_config()

    try:
        rfd = delete_file(params[0].strip(),config['cwdid'])
        if rfd["status_code"] == '200' and rfd["data"] is not None:
            print("File Deleted.")
        else:
            print(rfd["message"] )              
    except Exception as e:
        print(f"An error occurred: {e}")