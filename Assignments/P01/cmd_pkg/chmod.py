import os
import sys
from cmd_pkg.cmdsLogger import CmdsLogger

def chmod(**kwargs):
    cmds_logger = CmdsLogger()
    sys.stdout = cmds_logger

    try:
        params = kwargs.get("params",[])
        flags = kwargs.get("flags",[])

        # Check if MODE and FILE arguments are provided
        if not params:
            print("Error: Please provide at least one MODE and one FILE.")
            return ""
        
        # Separate the modes and files
        files = []
        modes = []

        for param in params:
            if os.path.exists(param):
                files.append(param)
            else:
                modes.append(param)

        if not files:
            print("Error: Please provide at least one valid FILE.")
            return ""

        for param in params: 
            try: 
                int_type_mode = int(modes,8)
                for file in files:
                    os.chmod(file, int_type_mode)  # Change the file mode
                    print(f"Changed mode of {file} to {oct(int_type_mode)[2:]}")

            except Exception as e:
                print(f"Error changing mode: {str(e)}")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        sys.stdout = sys.__stdout__

    captured_output = ''.join(cmds_logger.log_content)
    return captured_output


