from cmd_pkg.cmdsLogger import CmdsLogger
import os
import sys

def wc(**kwargs):

    cmds_logger = CmdsLogger()
    sys.stdout = cmds_logger
    try:
        params = kwargs.get("params", [])
        flags = kwargs.get("flags", [])
        input_text = kwargs.get("input",[])

        is_line_count  = 'l' in flags
        is_word_count =  'w' in flags

        if params:
            file = params[0]
            if os.path.isfile(file):
                with open(file, 'r') as f:
                    file_content = f.read()
                counts = content_count(file_content, is_line_count, is_word_count)
                print(f"{' '.join(map(str,counts))} {file}")

            else:
                counts = content_count(input_text, is_line_count, is_word_count)
                print(' '.join(map(str,counts)))

    except Exception as e:
        print(f"Error: {str(e)}")
        
    finally:
        sys.stdout = sys.__stdout__
        captured_output = "".join(cmds_logger.log_content)
        return captured_output

def content_count(text, isCountLine, isCountWord):
    
    # list comprehension create new list of non-empty lines, 
    # if line.strip(): This checks if the line is not empty (ignoring any whitespace).
    # The strip() method removes leading and trailing whitespace. If the line contains
    # only whitespace, it evaluates to False, so it is not included in the resulting list.
    # text.split('\n'): This splits the text string into a list of lines based on the 
    # newline character (\n).

    lines = len([line for line in text.split('\n') if line.strip()])
    words = len(text.split())
    characters = len(text)

    if isCountLine:
        return [lines]
    elif isCountWord:
        return [words]
    else:
        return [lines, words, characters]
