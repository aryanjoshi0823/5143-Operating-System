# Libraries for FastAPI
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime
import os
from random import shuffle
from random import choice
from sqliteCRUD import SqliteCRUD
import base64


# This is the `app` instance which passes in a series of keyword arguments
# configuring this instance of the api. The URL's are obviously fake.
app = FastAPI(
    title="File System",
    description="""🚀## File System Api""",
    version="0.0.1",
    terms_of_service="https://aryanjoshi.com/terms/",
    contact={
        "name": "FileSystemAPI",
        "url": "https://aryan.com/contact/",
        "email": "joshi@aryan.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

dataPath = "./"
dbName = "filesystem.db"
if os.path.exists(os.path.join(dataPath, dbName)):
    fileDB = SqliteCRUD(os.path.join(dataPath, dbName))
else:
    print("Database file not found.")
    fileDB = None

# """
# _____   ____  _    _ _______ ______  _____
#  |  __ \ / __ \| |  | |__   __|  ____|/ ____|
#  | |__) | |  | | |  | |  | |  | |__  | (___
#  |  _  /| |  | | |  | |  | |  |  __|  \___ \\
#  | | \ \| |__| | |__| |  | |  | |____ ____) |
#  |_|  \_\\____/ \____/   |_|  |______|_____/
# """


CURRENT_TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@app.get("/")
async def docs_redirect():
    """Api's base route that displays the information created above in the ApiInfo section."""
    return RedirectResponse(url="/docs")

@app.get("/tables/")
async def readFromAnyTable(pid: int = None,  table_name: str = None):
    """
    ### Description:
        Get a list of files in the directory passed by user.
    ### Params:
        id (int) :  id of table name user entered
    ### Returns:
        list : if id not present list all content of the table 
              otherwise return content with same id. 
    """

   # Pass the table name and optional id to readData
    files = fileDB.readTableDataByPid(table_name, pid)
    if files["success"]:
        return {"status_code": "200", "message": "", "data": files["data"]}
    return {"status_code": "404", "message": "File is empty or null", "data":[]}

@app.get("/getFileById")
def get_file_By_Id(id: int):
    """
    Reads the contents of a file and tracks the access in the database.
    :param filepath: The path of the file to read.
    """
    file = fileDB.readFileById(id)
    if file["success"] and file["data"]:
        read_permission =  file["data"][0][8]
        if read_permission == 1:
            return {"status_code": "200", "message": "", "data": file["data"][0]}
        return {"status_code": "404", "message": "No read access","data":[]}
    return {"status_code": "404", "message": "File not found","data":[]}

@app.get("/getDirById")
def get_Dir_By_Id(id: int):
    """
    Reads the contents of a file and tracks the access in the database.
    :param filepath: The path of the file to read.
    """
    dir = fileDB.readDirectoryById(id)
    if dir["success"] and dir["data"]:
        read_permission =  dir["data"][0][8]
        if read_permission == 1:
            return {"status_code": "200", "message": "", "data": dir["data"][0]}
        return {"status_code": "404", "message": "No read access","data":[]}
    return {"status_code": "404", "message": "Dir not found","data":[]}

@app.get("/getId")
async def get_id(path: str, curr_dir_id: int = 0):
    """
    Recursively find the pid of the path, supporting both absolute and relative paths.
    
    Args:
        path (str): The path to find the pid of.
        current_dir_pid (int, optional): The pid of the current directory (used for relative paths).
                                        Defaults to 1 (root directory).
     For instance,
        1. /python_code/ShapeModules/Point.pyc  --> already under root directory   
        2. Point.pyc only
        3. ShapeModules only etc.
    """

    if path == "/":
        return {"status_code": "200", "message": "", "data": 0} 
    
    params = [d for d in path.strip().split("/") if d]  
    final_component = params[-1]
    curr_id = curr_dir_id 

    # Traverse through directories and handle relative paths
    for param in params[:-1]:
        if param == "..":
            # Move up one directory
            parent_result = fileDB.run_query_in_thread([f"SELECT pid FROM directories WHERE id = '{curr_id}'"])[0]
            if parent_result["success"] and parent_result["data"]:
                curr_id = parent_result["data"][0][0]  # Update to parent directory id
            else:
                return {"status_code": "404", "message": f"Cannot move up from id '{curr_id}'", "data": []}
            
        elif param == ".":
            continue

        elif param == "~":
            curr_id = 1

        else:
            # Normal directory traversal
            query = f"SELECT id FROM directories WHERE name = '{param}' AND pid = '{curr_id}'"
            res = fileDB.run_query_in_thread([query])[0]

            if res["success"] and res["data"]:
                curr_id = res["data"][0][0]
            else:
                return {"status_code": "404", "message": f"Directory '{param}' not found.", "data": []}
            
    # check if it's a file
    result = fileDB.readFileByPid(final_component, curr_id)
    if result['data'] and result["success"]:
        return {"status_code": "200", "message": "", "data": result['data'][0][0], "type":"file"}

    # check if it's a directory
    dir_result = fileDB.getDirectoryId([final_component], curr_id)
    if dir_result["success"] and dir_result['data']:   
        return {"status_code": "200", "message": "", "data": dir_result['data'][0][0], "type":"dir"}
    
    if dir_result["data"] == [] and result["data"] == []:
        return {"status_code": "404", "message": f"File or Directory '{final_component}' not found.", "data": curr_id}

@app.get("/dirId")
def getDirId(dir: str, id: int = 0):
    """
    Get the directory id by name.
    
    Args:
        dir (str): The name of the directory (can be a path).
        id (int): The  id of the directory (defaults to 1 for root).
    
    Returns:
        dict: A dictionary with status code and directory id or error message.
    """
    temp_id = 0
    if dir == "/":
        return {"status_code": "200", "message": "", "data": 0} 
     
    dirs = [d for d in dir.strip().split("/") if d]  
    for part in dirs:
        if part == "..":
            # Move up one directory
            parent_result = fileDB.run_query_in_thread([f"SELECT pid FROM directories WHERE id = '{id}'"])[0]
            if parent_result["success"] and parent_result["data"]:
                temp_id = parent_result["data"][0][0]  # Update to parent directory id

        elif part == ".":
            continue

        elif part == "~":
            temp_id = 1

        else:
            # Normal directory traversal
            query = f"SELECT id FROM directories WHERE name = '{part}' AND pid = '{id}'"
            res = fileDB.run_query_in_thread([query])[0]

            if res["success"] and res["data"]:
                # Update the pid with the found directory's ID
                temp_id = res["data"][0][0]
            else:
                return {"status_code": "404", "message": f"Directory '{part}' not found.", "data": []}
    return {"status_code": "200", "message": "", "data": temp_id}


@app.get("/getHistory")
def get_history():
    vlu = fileDB.getHistory()
    if vlu["success"] and vlu["data"]:
        return {"status_code": "200", "message": "", "data": vlu["data"]}


@app.get("/file")
async def read_file_content(name: str, id: int = 0):
    """
    Reads the contents of a file and tracks the access in the database.
    :param filepath: The path of the file to read.
    """

    res = await get_id(name, id)
    if res["status_code"] == "200" and res["data"]:

        _id = res["data"]
        file = fileDB.readFileById(_id)

        if file["success"] and file["data"]:
            read_permission =  file["data"][0][8]
            if read_permission == 1:

                vlu = file["data"][0][7] 
                if vlu.startswith("b'") and vlu.endswith("'"):

                    vlu_cleaned = vlu[2:-1]  
                    base64_decoded = base64.b64decode(vlu_cleaned)
                    decoded_str = base64_decoded.decode("utf-8")


                    return {"status_code": "200", "message": "", "data": decoded_str }
            return {"status_code": "404", "message": "No read access","data":[]}
    return {"status_code": "404", "message": "File not found","data":[]}

@app.post("/postFile")
async def write_file_content(filepath:str, id:int, content:str):
    """
    Writes data to a file and logs the write operation in the database.
    :param filepath: The path of the file to write to.
    :param content: The content to write to the file. It overwrite the data.
    """
    res = await get_id(filepath, id)
    if res["status_code"] == "200" and res["data"]:

        content_bytes = content.encode('utf-8')  
        encoded_content = base64.b64encode(content_bytes) 

        fileDB.updateData("files", "contents", str(encoded_content), "id", res["data"])
        return {"status_code": "200", "message": "Files content are updated", "data":[]}
        
    elif res["status_code"] == "404" and res["data"]:

        files_params = filepath.split("/")
        _id = res["data"]
        file_part = files_params[-1]
  
        content_bytes = content.encode('utf-8')  
        encoded_content = base64.b64encode(content_bytes) 

        # Prepare data for insertion
        data = (None, _id, 1, file_part, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, str(encoded_content), 1, 1, 0, 0, 0, 0)
        response = fileDB.insertData("files", data)

        if response['success']:
            return {"status_code": "200", "message": f"Data written on '{files_params[-1]}' successfully", "data":[]}
        else:
            return {"status_code": "404", "message": f"File '{files_params[-1]}' creation unsuccessful", "data":[]}

@app.post("/history")
def add_cmd_history(cmds:str):
    """
    Writes data to a file and logs the write operation in the table History.
    :param filepath: The path of the file to write to.
    :param cmds: commands entered by users.
    """
    cmds_vlu = cmds.strip()
    data = (None, cmds_vlu, CURRENT_TIMESTAMP)
    response = fileDB.insertData("History", data)

    if response['success']:
        return {"status_code": "200", "message": f" '{cmds}' inserted successfully", "data":[]}
    else:
        return {"status_code": "404", "message": f"'{cmds}' insertion unsuccessful", "data":[]}


@app.post("/touch")
async def create_file(name: str, id: int):
    """
    Creates a new file in the filesystem and records the action in the database.
    :param filepath: The path where the file is to be created.
    - need to know current location id
    - need to know the name of the file
    - use current time to set created_at and modified_at
    - size will be 0
    """
    rf = await get_id(name, id)

    if rf["status_code"] == "200"  and rf["data"]:
        fileDB.updateData("files", "modified_at", CURRENT_TIMESTAMP, "id", rf["data"])
        return {"status_code": "200", "message": "File already exists, modified date updated.", "data":[]}

    else:
        files_params = name.split("/")
        _id = rf["data"]
        file_part = files_params[-1]
  
        # Prepare data for insertion
        data = (None, _id, 1, file_part, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, None, 1, 1, 0, 0, 0, 0)
        response = fileDB.insertData("files", data)

        if response['success']:
            return {"status_code": "200", "message": f"File '{files_params[-1]}' created successfully", "data":[]}
        else:
            return {"status_code": "404", "message": f"File '{files_params[-1]}' creation unsuccessful", "data":[]}
    
@app.post("/dir")
def create_directory(name: str, id: int = 1):
    """
    Creates a new directory in the filesystem and records the action in the database.
    :param directory_path: The path of the directory to be created.
    """
    rd = getDirId(name, id)

    # in case directory already existed.
    if rd["status_code"] and rd["data"]:
        fileDB.updateData("directories", "modified_at", CURRENT_TIMESTAMP, "id", rd["data"])
        return {"status_code": "200", "message": "Directory already exists, modified date updated.", "data":[]}
    else:
        dirs = name.split("/")
        _id = id

        for dir in dirs[:-1]:
            if dir: 
                result = getDirId(dir, _id)
                if result['status_code'] == "200":
                    _id = result['data']
                else:
                    return {"status_code": "404", "message": f"Parent directory '{dir}' not found.", "data": []}

        # Prepare data for insertion
        data = (None, _id, 1, dirs[-1], CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1, 1, 1, 1, 0, 1)
        response = fileDB.insertData("directories", data)

        if response['success']:
            return {"status_code": "200", "message": f"Directory '{dirs[-1]}' created successfully", "data":[]}
        else:
            return {"status_code": "404", "message": f"Directory '{dirs[-1]}' creation unsuccessful", "data":[]}

@app.get("/dir")
def list_directory_Content(id: int):
    """
    Lists the contents of a directory and logs the access in the database.
    :param directory_path: The path of the directory to be listed.
    """
    files = fileDB.readDirContentByPid(id)
    if files["success"]:
        return {"status_code": "200", "message": "", "data": files["data"]}
    return {"status_code": "404", "message": "Directory is empty or null", "data":[]}
   
@app.get("/cp")
async def copy_file(src_name: str, dest_name: str,id):
    """
    Copies a file from one location to another and logs it in the database.
    :param src_path: The source file path.
    :param dest_path: The destination file path.
    """
    # check it in file table
    rf = await get_id(src_name, id)
    if rf["status_code"] == "200"  and rf["data"]:

        src_file = fileDB.readFileById(rf["data"])
        if  src_file["success"] and src_file["data"]:
            file_wr_permission =  src_file["data"][0][9]

            dir_id = await get_id(dest_name, id)
            dest_dir = fileDB.readDirectoryById(dir_id["data"])
            if  dest_dir["success"] and dest_dir["data"]:
                dir_wr_permission =  dest_dir["data"][0][7]

                if file_wr_permission == 1 and dir_wr_permission == 1:

                    data = (
                        None, 
                        dest_dir["data"][0][0],
                        1, 
                        src_name, 
                        src_file["data"][0][4],
                        CURRENT_TIMESTAMP, 
                        CURRENT_TIMESTAMP, 
                        src_file["data"][0][7], 
                        1, 
                        1, 
                        0, 
                        0, 
                        0, 
                        0
                    )
                    response = fileDB.insertData("files", data)
                    if response['success']:
                        return {"status_code": "200", "message": "File copied successfully", "data":[]}
                    else:
                        return {"status_code": "404", "message": "Coping file is unsuccessful", "data":[]}
                else: 
                    return {"status_code": "404", "message": "No write access", "data":[]}
            else:
                return {"status_code": "404", "message": "Destination Directory not found", "data":[]}
    else:
        return {"status_code": "404", "message": "Source file not found.", "data":[]}
        
@app.get("/mv")
async def move_file(src_name: str, dest_name: str, id):
    """
    Moves a file from one location to another and updates the database.
    :param src_path: The current file path.
    :param dest_path: The new file path.
    """
    # check it in file table
    rf = await get_id(src_name, id)
    if rf["status_code"] == "200"  and rf["data"]:

        src__wr_permission = 0
        src_file = ""
        src_dir = ""

        if rf["type"] == "file":
            src_file = fileDB.readFileById(rf["data"])
            if  src_file["success"] and src_file["data"]:
                src__wr_permission =  src_file["data"][0][9]
        
        if rf["type"] == "dir":
            src_dir = fileDB.readDirectoryById(rf["data"])

            if  src_dir["success"] and src_dir["data"]:
                src__wr_permission = src_dir["data"][0][7]
    
        if src__wr_permission:

            dir_id = await get_id(dest_name, id)
            if dir_id["status_code"] == "200" and dir_id["data"]and dir_id["type"] == "dir":
                dest_dir = fileDB.readDirectoryById(dir_id["data"])

                if  dest_dir["success"] and dest_dir["data"]:
                    dir_wr_permission =  dest_dir["data"][0][7]
                    
                    if src__wr_permission == 1 and dir_wr_permission == 1:
                        if  rf["type"] == "file":
                            fileDB.updateData("files", "pid", dest_dir["data"][0][0], "id", src_file["data"][0][0])
                            return {"status_code": "200", "message": "Source file is moved to destination directory", "data":[]}

                        else:
                            fileDB.updateData("directories", "pid", dest_dir["data"][0][0], "id", src_dir["data"][0][0])
                            return {"status_code": "200", "message": "Source directory is moved to destination directory", "data":[]}

                    else: 
                        return {"status_code": "404", "message": "No write access", "data":[]}   
            else:
                return {"status_code": "404", "message": "Destination not found", "data":"dError"}
    else:
        return {"status_code": "404", "message": "Source not found.", "data":""}

@app.get("/perm_file")
async def get_file_permissions(name:str, id:int):
    """
    Retrieves the permissions of a file and logs the action in the database.
    :param filepath: The path of the file.
    """
    #/python_code/ShapeModules/Point.pyc 
    res = await get_id(name, id)
    if res["status_code"] == "200" and res["data"]:
        files_params = name.split("/")
        _id = res["data"]
        file_part = files_params[-1].strip()
        file = fileDB.getFilePermission(file_part,_id)

        if file["success"] and file["data"]:
            return {"status_code": "200", "message": "", "data": file["data"][0]}
    return {"status_code": "404", "message": "File not found","data":[]}

@app.get("/perm_dir")
async def get_file_permissions(name:str, id:int):
    """
    Retrieves the permissions of a file and logs the action in the database.
    :param dirpath: The path of the file.
    """
    #/python_code/ShapeModules/Point.pyc 
    res = await get_id(name, id)
    if res["status_code"] == "200" and res["data"]:
        files_params = name.split("/")
        _id = res["data"]
        file_part = files_params[-1].strip()
        file = fileDB.getDirPermission(file_part,_id)

        if file["success"] and file["data"]:
            return {"status_code": "200", "message": "", "data": file["data"][0]}
    return {"status_code": "404", "message": "File not found","data":[]}

# File Rename
@app.put("/mv")
async def rename_file(old_filepath:str, new_name:str, id:int):
    """
    Renames a file in the filesystem and updates the database with the new name.
    :param old_filepath: The current file path.
    :param new_filepath: The new file path.
    """
    rf = await get_id(old_filepath, id)
    if rf["status_code"] == "200" and rf["data"]:

        file = fileDB.readFileById(rf["data"])
        if file["success"] and file["data"]:
            write_permission =  file["data"][0][9]
            if write_permission == 1:
                fileDB.updateData("files", "name", new_name, "id", file["data"][0][0])
                return {"status_code": "200", "message": "File is renamed", "data":[]}
        
        return {"status_code": "404", "message": "No write access","data":[]}
    return {"status_code": "404", "message": "File not found","data":[]}

@app.put("/chmod_files")
async def set_file_permissions(name:str, id:int, r:int, w:int, e:int, wr: int, ww:int, we:int):
    """
    Sets the permissions of a file and logs the action in the database.
    :param filepath: The path of the file.
    :param permissions: The new permissions to set.
    """

    res = await get_id(name, id)

    if res["status_code"] == "200" and res["data"]:
        files_params = name.split("/")
        _id = res["data"]

        file_part = files_params[-1].strip()
        file = fileDB.updateFilePermission(file_part, _id, r, w, e, wr, ww, we)
        if file["success"]:
            return {"status_code": "200", "message": "File permission updated", "data":[]}
    return {"status_code": "404", "message": "File not found","data":[]}

@app.put("/chmod_dirs")
async def set_dir_permissions(name:str, id:int, r:int, w:int, e:int, wr: int, ww:int, we:int):
    """
    Sets the permissions of a file and logs the action in the database.
    :param dirpath: The path of the file.
    :param permissions: The new permissions to set.
    """
    res = await get_id(name, id)
    if res["status_code"] == "200" and res["data"]:

        files_params = name.split("/")
        _id = res["data"]
        file_part = files_params[-1].strip()

        file = fileDB.updateDirPermission(file_part, _id, r, w, e, wr, ww, we)
        if file["success"]:
            return {"status_code": "200", "message": "Dir permission updated", "data":[]}
    return {"status_code": "404", "message": "Dir not found","data":[]}

@app.delete("/rm")
async def delete_file(name: str, id: int):
    """
        Deletes a file from the database and the filesystem.
        :param name: Name of the file
        :param pid: Parent directory ID
    """     
    rf = await get_id(name, id)
    if rf["status_code"] == "200" and rf["data"]:

        file = fileDB.readFileById(rf["data"])
        if file["success"] and file["data"]:
            fileDB.deleteData("files", "id", file["data"][0][0])
        return {"status_code": "200", "message": f"File '{name}' deleted successfully","data":[]}
    
    return {"status_code": "404", "message": f"File not found", "data":[]}


if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8080, log_level="debug", reload=True)


# converted_object = ast.literal_eval(string_representation)
# print("Converted back to object:", converted_object)