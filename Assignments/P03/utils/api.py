import requests
from rich import print

def getConfig(client_id):
    return {
        "client_id": client_id,
        "min_jobs": 5,
        "max_jobs": 5,
        "min_bursts": 5,
        "max_bursts": 10,
        "min_job_interval": 1,
        "max_job_interval": 2,
        "burst_type_ratio": 0.5,
        "min_cpu_burst_interval": 10,
        "max_cpu_burst_interval": 30,
        "min_io_burst_interval": 10,
        "max_io_burst_interval": 30,
        "min_ts_interval": 10,
        "max_ts_interval": 10,
        "priority_levels": [1, 2, 3, 4, 5] 
    }

def init(config):
    """
    This function will initialize the client and return the `client_id` and `session_id`
    """
    route = f"http://profgriffin.com:8000/init"
    r = requests.post(route,json=config)
    if r.status_code == 200:
        response = r.json()
        return response
    else:
        print(f"Error: {r.status_code}")
        return None


def getJob(client_id,session_id,clock_time):  
    route = f"http://profgriffin.com:8000/job?client_id={client_id}&session_id={session_id}&clock_time={clock_time}"
    r = requests.get(route)
    if r.status_code == 200:
        response = r.json()
        return response
    else:
        print(f"Error: {r.status_code}")
        return None
    
def getBurst(client_id, session_id, job_id):
    route = f"http://profgriffin.com:8000/burst?client_id={client_id}&session_id={session_id}&job_id={job_id}"
    r = requests.get(route)
    if r.status_code == 200:
        response = r.json()
        return response
    else:
        print(f"Error: {r.status_code}")
        return None
    
def getBurstsLeft(client_id, session_id, job_id):
    route = f"http://profgriffin.com:8000/burstsLeft?client_id={client_id}&session_id={session_id}&job_id={job_id}"
    r = requests.get(route)
    if r.status_code == 200:
        response = r.json()
        return response
    else:
        print(f"Error: {r.status_code}")
        return None

def getJobsLeft(client_id, session_id):
    route = f"http://profgriffin.com:8000/jobsLeft?client_id={client_id}&session_id={session_id}"
    r = requests.get(route)
    if r.status_code == 200:
        response = r.json()
        return response
    else:
        print(f"Error: {r.status_code}")
        return None