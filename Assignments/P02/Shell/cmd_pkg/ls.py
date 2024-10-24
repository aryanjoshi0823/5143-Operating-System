from helper_files.api_call import *
from helper_files.utils import *
from helper_files.rich_format import print_rich_table 

#import humanize

def ls(**kwargs):

    input = kwargs["input"] if kwargs.get("input") else []
    params = kwargs["params"] if kwargs.get("params") else []
    flags = kwargs["flags"] if kwargs.get("flags") else []

    config = load_config()

    print('\r')
    
    #help not executed

    if input:
        try: 
            dir_res = get_dir_content(config['cwdid'])
            if dir_res["status_code"] == '200' and dir_res["data"] is not None:

                headers = [] 
                data = []
                
                # Apply filtering for dot files based on flags
                if 'a' in flags or 'lah' in flags:
                    filtered_data = dir_res["data"]  
                else:
                    filtered_data = [item for item in dir_res["data"] if not str(item[3]).startswith('.')] 

                # Prepare common fields
                permission_formats = [format_permissions(item[7:14]) for item in filtered_data]
                h_r_size = [human_readable_size(item[4]) for item in filtered_data]
                last_modified_date = [format_time(item[6]) for item in filtered_data]
                name_vlu = [str(item[3]) for item in filtered_data]


                if not flags:
                    headers.append("File and Directory Name")
                    for i in range(len(filtered_data)):
                        row = [name_vlu[i]]
                        data.append(row)

                if 'lah' in flags:
                    headers.extend(["Permission", "User", "Size", "Last_Modified", "Name"])
                    for i in range(len(filtered_data)):
                        row = [permission_formats[i], config["user"], h_r_size[i], last_modified_date[i], name_vlu[i]]
                        data.append(row)

                elif 'a' in flags: 
                    headers.append("File and Directory Name")
                    for i in range(len(filtered_data)):
                        row = [name_vlu[i]]
                        data.append(row)

                elif 'h' in flags:
                    headers.extend(["Permission", "User", "Size", "Last_Modified", "Name"])
                    for i in range(len(filtered_data)):
                        row = [permission_formats[i], config["user"], h_r_size[i], last_modified_date[i], name_vlu[i]]
                        data.append(row)

                elif 'l' in flags:
                    headers.extend(["Permission", "User", "Size", "Last_Modified", "Name"])
                    size = []
                    for item in filtered_data:
                        if  item[4] is None:
                            size.append("-")
                        else:
                            size.append(str(item[4]) )

                    for i in range(len(filtered_data)):
                        row = [permission_formats[i], config["user"], size[i], last_modified_date[i], name_vlu[i]]
                        data.append(row)

                print_rich_table(headers, data)
                return(str(data))

            else:
                print(dir_res['message'])

        except Exception as e:
            print(f"Error: {e}")



    


