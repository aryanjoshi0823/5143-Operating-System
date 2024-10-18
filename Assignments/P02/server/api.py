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
from utility import *
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
#   _____   ____  _    _ _______ ______  _____
#  |  __ \ / __ \| |  | |__   __|  ____|/ ____|
#  | |__) | |  | | |  | |  | |  | |__  | (___
#  |  _  /| |  | | |  | |  | |  |  __|  \___ \\
#  | | \ \| |__| | |__| |  | |  | |____ ____) |
#  |_|  \_\\____/ \____/   |_|  |______|_____/

#  This is where your routes will be defined. Remember they are really just python functions
#  that will talk to whatever class you write above. Fast Api simply takes your python results
#  and packages them so they can be sent back to your programs request.
# """


CURRENT_TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@app.get("/")
async def docs_redirect():
    """Api's base route that displays the information created above in the ApiInfo section."""
    return RedirectResponse(url="/docs")

@app.get("/files/")
async def getContent(pid: int = None,  table_name: str = None):
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
    files = fileDB.readData(table_name, pid)
    if files["success"]:
        return {"status_code": "200", "message": "", "data": files["data"]}
    return {"status_code": "404", "message": "File is empty or null", "data":[]}


@app.post("/touch")
def create_file(name: str, pid: int):
    """
    Creates a new file in the filesystem and records the action in the database.
    :param filepath: The path where the file is to be created.
    - need to know current location id
    - need to know the name of the file
    - use current time to set created_at and modified_at
    - size will be 0
    """
    rd = fileDB.readFile(name, pid)
    if rd["success"] and rd["data"]:
        fileDB.updateData("files", "modified_at", CURRENT_TIMESTAMP, "id", rd["data"][0])
        return {"status_code": "200", "message": "File already exists, modified date updated.", "data":[]}

    # Prepare data for insertion
    data = (None, pid, 1, name, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, None, 1, 1, 0, 0, 0, 0)
    response = fileDB.insertData("files", data)

    if response['success']:
        return {"status_code": "200", "message": "File '{name}' created successfully", "data":[]}
    else:
        return {"status_code": "404", "message": "File '{name}' creation unsuccessful", "data":[]}


@app.get("/getPid")
async def get_Pid(path: str, curr_dir_pid: int = 1):
    """
    Recursively find the pid of the path, supporting both absolute and relative paths.
    
    Args:
        path (str): The path to find the pid of.
        current_dir_pid (int, optional): The pid of the current directory (used for relative paths).
                                        Defaults to 1 (root directory).
     For instance,
        1. /python_code/ShapeModules/Point.pyc  --> already under root directory   
        2. Point.pyc only
        3. ShapeModules only
        4. 
            /python_code/MyRTree
            /python_code/ShapeMod  --> pid 1  r to l
            /python_code/ShapeModules/..  ,   --> pid 1
            /python_code/ShapeModules/../../  --> pid 1
    """
    params = [d for d in path.strip().split("/") if d]  
    print("params-->",params)

    curr_pid = curr_dir_pid 

    # Traverse through directories and handle relative paths
    for param in params[:-1]:
        if param == "..":
            # Move up one directory
            parent_result = fileDB.run_query_in_thread([f"SELECT pid FROM directories WHERE id = '{curr_pid}'"])[0]
            if parent_result["success"] and parent_result["data"]:
                curr_pid = parent_result["data"][0][0]  # Update to parent directory id
            else:
                return {"status_code": "404", "message": f"Cannot move up from pid '{curr_pid}'", "data": []}
            
        elif param == ".":
            continue

        else:
            # Normal directory traversal
            query = f"SELECT id FROM directories WHERE name = '{param}' AND pid = '{curr_pid}'"
            res = fileDB.run_query_in_thread([query])[0]

            if res["success"] and res["data"]:
                curr_pid = res["data"][0][0]
            else:
                return {"status_code": "404", "message": f"Directory '{param}' not found.", "data": []}
    
    # final component 
    final_component = params[-1]
    
    # check if it's a file
    result = fileDB.readFile(final_component, curr_pid)
    if result['data'] and result["success"]:
        return {"pid": result['data'][0][0]}  

    # check if it's a directory
    dir_result = fileDB.getDirectoryId([final_component], curr_pid)
    if dir_result['data']:
        return {"pid": dir_result['data'][0][0]}  
    
    return {"error": f"File or directory '{final_component}' not found in pid '{curr_pid}'."}



@app.get("/dirId")
def getDirId(dir: str, pid: int = 1):
    """
    Get the directory id by name.
    
    Args:
        dir (str): The name of the directory (can be a path).
        pid (int): The parent id of the directory (defaults to 1 for root).
    
    Returns:
        dict: A dictionary with status code and directory id or error message.
    """
    # Split the directory path into parts
    dirs = [d for d in dir.strip().split("/") if d]  
    print(dirs)
    # Traverse each directory in the path
    for part in dirs:
        if part == "..":
            # Move up one directory
            parent_result = fileDB.run_query_in_thread([f"SELECT pid FROM directories WHERE id = '{pid}'"])[0]
            if parent_result["success"] and parent_result["data"]:
                pid = parent_result["data"][0][0]  # Update to parent directory id
            else:
                return {"status_code": "404", "message": f"Cannot move up from pid '{pid}'", "data": []}
        elif part == ".":
            # Current directory, ignore and continue
            continue
        else:
            # Normal directory traversal
            query = f"SELECT id FROM directories WHERE name = '{part}' AND pid = '{pid}'"
            res = fileDB.run_query_in_thread([query])[0]

            if res["success"] and res["data"]:
                # Update the pid with the found directory's ID
                pid = res["data"][0][0]
            else:
                return {"status_code": "404", "message": f"Directory '{part}' not found.", "data": []}

    return {"status_code": "200", "message": "", "data": pid}


### 2. **File Deletion**
@app.delete("/rm")
def delete_file(name: str, pid: int):
    """
        Deletes a file from the database and the filesystem.
        :param name: Name of the file
        :param pid: Parent directory ID
    """
    file = fileDB.readFile(name, pid)

    if file["success"] and file["data"]:
        fileDB.deleteData("files", "id", file["data"][0][0])
        return {"status_code": "200", "message": f"File '{name}' deleted successfully","data":[]}
    
    return {"status_code": "404", "message": f"File not found", "data":[]}


### 3. **File Read**
@app.get("/file")
def read_file_content(filepath: str, pid: int):
    """
    Reads the contents of a file and tracks the access in the database.
    :param filepath: The path of the file to read.
    """
    file = fileDB.readFile(filepath, pid)
    if file["success"] and file["data"]:
        read_permission =  file["data"][0][8]
        if read_permission == 1:
                return {"status_code": "200", "message": "", "data": file["data"][0][7]}
        return {"status_code": "404", "message": "No read access","data":[]}
    return {"status_code": "404", "message": "File not found","data":[]}


### 4. **File Write**
@app.post("/postFile")
def write_file_content(filepath:str, pid:int, content:str):
    """
    Writes data to a file and logs the write operation in the database.
    :param filepath: The path of the file to write to.
    :param content: The content to write to the file.
    """
    file = fileDB.readFile(filepath, pid)
    print(file)
    if file["success"] and file["data"]:
        write_permission =  file["data"][0][9]

        if write_permission == 1:

            if isinstance(content, str):
                content_bytes = content.encode('utf-8')  # Convert string to bytes
                print(content_bytes)
                encoded_content = base64.b64encode(content_bytes) # Encode to Base64
                print(encoded_content)
            else:
                return {"status_code": "400", "message": "Content must be a string", "data": []}
            

            fileDB.updateData("files", "contents", encoded_content, "id", file["data"][0][0])
            return {"status_code": "200", "message": "Files content are updated", "data":[]}
        
        return {"status_code": "404", "message": "No write access","data":[]}
    return {"status_code": "404", "message": "File not found","data":[]}



### 5. **File Rename**
@app.put("/mv")
def rename_file(old_filepath:str, new_filepath:str, pid:int):
    """
    Renames a file in the filesystem and updates the database with the new name.
    :param old_filepath: The current file path.
    :param new_filepath: The new file path.
    """
    # TODO: Rename the file and update the DB with the new path.
    # db.update_filename(old_filepath, new_filepath)
    file = fileDB.readFile(old_filepath, pid)
    if file["success"] and file["data"]:
        write_permission =  file["data"][0][9]
        if write_permission == 1:
            fileDB.updateData("files", "name", new_filepath, "id", file["data"][0][0])
            return {"status_code": "200", "message": "File is renamed", "data":[]}
        
        return {"status_code": "404", "message": "No write access","data":[]}
    return {"status_code": "404", "message": "File not found","data":[]}



### 6. **Directory Creation**
@app.post("/dir")
def create_directory(name: str, pid: int = 1):
    """
    Creates a new directory in the filesystem and records the action in the database.
    :param directory_path: The path of the directory to be created.
    """
    rd = fileDB.readDirectories(name, pid)
    if rd["success"] and rd["data"]:
        fileDB.updateData("directories", "modified_at", CURRENT_TIMESTAMP, "id", rd["data"][0])
        return {"status_code": "200", "message": "Directory already exists, modified date updated.", "data":[]}

    # Prepare data for insertion
    data = (None, pid, 1, name, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1, 1, 1, 1, 0, 1)
    response = fileDB.insertData("directories", data)

    if response['success']:
        return {"status_code": "200", "message": f"Directory '{name}' created successfully", "data":[]}
    else:
        return {"status_code": "404", "message": f"Directory '{name}' creation unsuccessful", "data":[]}


### 7. **Directory Deletion**
@app.delete("/dir")
def delete_directory(name: str, pid: int):
    """
    Deletes a directory and its contents from the filesystem and records it in the database.
    :param directory_path: The path of the directory to be deleted.
    """
    dir = fileDB.readDirectories(name, pid)

    if dir["success"] and dir["data"]:
        fileDB.deleteData("directories", "id", dir["data"][0][0])
        return {"status_code": "200", "message": f"Directory '{name}' deleted successfully","data":[]}
    
    return {"status_code": "404", "message": f"Directory not found", "data":[]}


## need to do.
### 8. **Directory Listing**
@app.get("/dir")
def list_directory(dir_name: str, pid: int):
    """
    Lists the contents of a directory and logs the access in the database.
    :param directory_path: The path of the directory to be listed.
    """
    # TODO: Retrieve all files/directories and log the action in the DB.
    # db.insert_action(directory_path, "listed")
    # files = fileDB.readDirectories(dir_name, pid)
    # if files["success"] and files["data"]:
    #     return {"status_code": "200", "message": "", "data": files["data"]}
    # return {"status_code": "404", "message": "File is empty or null", "data":[]}


### 9. **File Copy**


@app.get("/cp")
def copy_file(src_id: int, dest_id: int, new_name: str):
    """
    Copies a file from one location to another and logs it in the database.
    :param src_path: The source file path.
    :param dest_path: The destination file path.
    """
    # check it in file table
    src_file = fileDB.readFileById(src_id)
    if  src_file["success"] and src_file["data"]:
            file_wr_permission =  src_file["data"][0][9]

            dest_dir = fileDB.readDirectoryById(dest_id)
            if  dest_dir["success"] and dest_dir["data"]:
                dir_wr_permission =  dest_dir["data"][0][7]

                if file_wr_permission == 1 and dir_wr_permission == 1:

                    data = (
                        None, 
                        dest_dir["data"][0][0],
                        1, 
                        new_name, 
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
                    print(data)
                    response = fileDB.insertData("files", data)
                    if response['success']:
                        return {"status_code": "200", "message": "File '{name}' copied successfully", "data":[]}
                    else:
                        return {"status_code": "404", "message": "Coping file '{name}' is unsuccessful", "data":[]}
                else: 
                    return {"status_code": "404", "message": "No write access", "data":[]}
            else:
                return {"status_code": "404", "message": "Destination Directory not found", "data":[]}
        #else:
            #check it in directories table.
    else:
        return {"status_code": "404", "message": "Source file not found.", "data":[]}
        

### 10. **File Move**
@app.get("/mv")
def move_file(src_id: int, dest_id: int):
    """
    Moves a file from one location to another and updates the database.
    :param src_path: The current file path.
    :param dest_path: The new file path.
    """
    # check it in file table
    src_file = fileDB.readFileById(src_id)
    if  src_file["success"] and src_file["data"]:
            file_wr_permission =  src_file["data"][0][9]

            dest_dir = fileDB.readDirectoryById(dest_id)
            if  dest_dir["success"] and dest_dir["data"]:
                dir_wr_permission =  dest_dir["data"][0][7]

                if file_wr_permission == 1 and dir_wr_permission == 1:
                    fileDB.updateData("files", "pid", dest_dir["data"][0][0], "id", src_file["data"][0][0])
                    return {"status_code": "200", "message": "File is moved to destination directory", "data":[]}
                else: 
                    return {"status_code": "404", "message": "No write access", "data":[]}
            else:
                return {"status_code": "404", "message": "Destination Directory not found", "data":[]}
        #else:
            #check it in directories table.
    else:
        return {"status_code": "404", "message": "Source file not found.", "data":[]}


### 11. **File Permissions**
@app.get("/perm")
def get_file_permissions(name:str, pid:int):
    """
    Retrieves the permissions of a file and logs the action in the database.
    :param filepath: The path of the file.
    """
    file = fileDB.getFilePermission(name, pid)
    if file["success"] and file["data"]:
        return {"status_code": "200", "message": "", "data": file["data"][0]}
    return {"status_code": "404", "message": "File not found","data":[]}


@app.put("/chmod")
def set_file_permissions(name:str, pid:int, r:int, w:int, e:int, wr: int, ww:int, we:int):
    """
    Sets the permissions of a file and logs the action in the database.
    :param filepath: The path of the file.
    :param permissions: The new permissions to set.
    """
    file = fileDB.updateFilePermission(name, pid, r, w, e, wr, ww, we)
    if file["success"]:
        return {"status_code": "200", "message": "File permission updated", "data":[]}
    return {"status_code": "404", "message": "File not found","data":[]}


if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8080, log_level="debug", reload=True)
