
import requests

base_url = "http://127.0.0.1:8080/"

def get_directory_id(dir: str, id: int ):

    api_url = f"{base_url}dirId?dir={dir}&id={id}"
    response = requests.get(api_url)

    if response.status_code == 200:
        return response.json() 
    else:
        return {"status_code": response.status_code, "message": response.json().get("message")}

def get_dir_content(id: int ):
    
    api_url = f"{base_url}dir?id={id}"
    response = requests.get(api_url)

    if response.status_code == 200:
        return response.json() 
    else:
        return {"status_code": response.status_code, "message": response.json().get("message")}
    
def get_dir(id: int ):
    api_url = f"{base_url}getDirById?id={id}"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json() 
    else:
        return {"status_code": response.status_code, "message": response.json().get("message")}
    
def make_directory(param: str, id: int):
    api_url = f"{base_url}dir?name={param}&id={id}"
    response = requests.post(api_url)
    if response.status_code == 200:
        return response.json() 
    else:
        return {"status_code": response.status_code, "message": response.json().get("message")}
    
def make_file(param: str, id: int):
    api_url = f"{base_url}touch?name={param}&id={id}"
    response = requests.post(api_url)
    if response.status_code == 200:
        return response.json() 
    else:
        return {"status_code": response.status_code, "message": response.json().get("message")}
    
def read_file_data(param: str, id: int): 
    api_url = f"{base_url}file?name={param}&id={id}"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json() 
    else:
        return {"status_code": response.status_code, "message": response.json().get("message")}
    
def get_file_permission(param: str, id: int):
    api_url = f"{base_url}perm_file?name={param}&id={id}"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json() 
    else:
        return {"status_code": response.status_code, "message": response.json().get("message")}
    
def get_dir_permission(param: str, id: int): 
    api_url = f"{base_url}perm_dir?name={param}&id={id}"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json() 
    else:
        return {"status_code": response.status_code, "message": response.json().get("message")}
    
def copy_file(src_name: str, dest_name: str, new_name: str, id):
    api_url = f"{base_url}cp?src_name={src_name}&dest_name={dest_name}&new_name={new_name}&id={id}"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json() 
    else:
        return {"status_code": response.status_code, "message": response.json().get("message")}

def mv_file(src_name: str, dest_name: str, id):
    api_url = f"{base_url}mv?src_name={src_name}&dest_name={dest_name}&id={id}"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json() 
    else:
        return {"status_code": response.status_code, "message": response.json().get("message")}

def rename_file(old_filepath: str, new_name: str, id):
    api_url = f"{base_url}mv?old_filepath={old_filepath}&new_name={new_name}&id={id}"
    response = requests.put(api_url)
    if response.status_code == 200:
        return response.json() 
    else:
        return {"status_code": response.status_code, "message": response.json().get("message")}

def update_file_permission(param: str, id: int, perm): 
    api_url = f"{base_url}chmod_files?name={param}&id={id}&r={perm[0]}&w={perm[1]}&e={perm[2]}&wr={perm[3]}&ww={perm[4]}&we={perm[5]}"
    response = requests.put(api_url)
    if response.status_code == 200:
        return response.json() 
    else:
        return {"status_code": response.status_code, "message": response.json().get("message")}
    
def update_dir_permission(param: str, id: int, perm):
    api_url = f"{base_url}chmod_dirs?name={param}&id={id}&r={perm[0]}&w={perm[1]}&e={perm[2]}&wr={perm[3]}&ww={perm[4]}&we={perm[5]}"
    response = requests.put(api_url)
    if response.status_code == 200:
        return response.json() 
    else:
        return {"status_code": response.status_code, "message": response.json().get("message")}
    
def update_history(cmds:str):
    api_url = f"{base_url}chmod_dirs?filepath=python_code/History&id=1&content={cmds}"
    response = requests.post(api_url)
    if response.status_code == 200:
        return response.json() 
    else:
        return {"status_code": response.status_code, "message": response.json().get("message")}
    
def delete_file(name: str, id: int):
    api_url = f"{base_url}rm?name={name}&id={id}"
    response = requests.delete(api_url)
    if response.status_code == 200:
        return response.json() 
    else:
        return {"status_code": response.status_code, "message": response.json().get("message")}