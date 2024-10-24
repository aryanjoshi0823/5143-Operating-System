from helper_files.api_call import *
from helper_files.utils import *

def whoami(**kwargs):
    config = load_config()
    print(config["user"])


