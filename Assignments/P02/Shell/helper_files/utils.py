import json
import datetime


def load_config():
    with open('.config', 'r') as config_file:
        return json.load(config_file)
    
def save_config(config):
    with open('.config', 'w') as config_file:
        json.dump(config, config_file, indent=4)

# Helper function to format file size in human-readable form
def human_readable_size(size):
    if size is None:
        return "-"
    for unit in ['B', 'K', 'M', 'G', 'T']:
        if size < 1024:
            return f"{size:.1f}{unit}"
        size /= 1024

# Function to format timestamp
def format_time(timestamp):
    if timestamp is None:
        return "-"
    dt = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    return dt.strftime('%b %d %H:%M')

def format_permissions(entry):
    # Check if it's a directory or a file
    perm = ['d' if entry[6] == 'directory' else '-']
    
    # User permissions
    perm.append('r' if entry[0] else '-')
    perm.append('w' if entry[1] else '-')
    perm.append('x' if entry[2] else '-')
    
    # Group permissions (world-readable, world-writable, world-executable)
    perm.append('r' if entry[3] else '-')
    perm.append('w' if entry[4] else '-')
    perm.append('x' if entry[5] else '-')
    
    return ''.join(perm)

def convert_mode_to_perm(mode):
    
    """
    Translates the given mode (numeric string) to the binary permission
    bits and applies it to the current permission settings.
    """
    # Convert the mode to a string of 3 digits (e.g., 755 -> '755')
    mode_str = str(mode).zfill(2)

    # Break mode into user, group
    user_mode = int(mode_str[0])
    group_mode = int(mode_str[1])

    # Convert each mode digit to binary and map to current permission structure
    user_perms = [int(x) for x in format(user_mode, '03b')]  # 3 bits for rwx
    group_perms = [int(x) for x in format(group_mode, '03b')]  # 3 bits for rwx

    # Concatenate new permissions as [user_r, user_w, user_x, group_r, group_w, group_x, others_r, others_w, others_x]
    new_perms = user_perms + group_perms 
    return new_perms

