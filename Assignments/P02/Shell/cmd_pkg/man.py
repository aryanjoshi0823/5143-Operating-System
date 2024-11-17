import sys
from helper_files.docstrings import *
from helper_files.cmdsLogger import PrintCaptureLogger

def man(**kwargs):
    print_capture_logger = PrintCaptureLogger()
    sys.stdout = print_capture_logger

    try: 
        params = kwargs["params"] if kwargs.get("params") else []
        flags = kwargs["flags"] if kwargs.get("flags") else []
        input = kwargs["input"] if kwargs.get("input") else []

        print('\r')

        if params and input==[] and flags==[]: 
            if len(params)>1:
                print("Error: more than one parameter.")
            elif'cd' in params:
                print(cd_doc)
            elif 'chmod' in params:
                print(chmod_doc)
            elif 'clear' in params:
                print(clear_doc)
            elif 'echo' in params:
                print(echo_doc)
            elif 'exit' in params:
                print(exit_doc)
            elif 'cat' in params:
                print(cat_doc)
            elif 'head' in params:
                print(head_doc)
            elif 'tail' in params:
                print(tail_doc)
            elif 'touch' in params:
                print(touch_doc)
            elif 'less' in params:
                print(less_doc)
            elif 'mv' in params:
                print(mv_doc)
            elif 'cp' in params:
                print(cp_doc)
            elif 'rm' in params:
                print(rm_doc)
            elif 'grep' in params:
                print(grep_doc)
            elif 'history' in params:
                print(history_doc)
            elif 'ls' in params:
                print(ls_doc)
            elif 'mkdir' in params:
                print(mkdir_doc)
            elif 'pwd' in params:
                print(pwd_doc)
            elif 'sort' in params:
                print(sort_doc)
            elif 'wc' in params:
                print(wc_doc)
            elif 'whoami' in params:
                print(whoami_doc)
            else:
                print(f"Command '{params[0]}' not found.")

        elif input or flags:
            pass

    finally:
        sys.stdout = sys.__stdout__  # Restore the original stdout

    captured_output = ''.join(print_capture_logger.log_content)
    return captured_output
        



