import sys
from helper_files.api_call import *
from helper_files.utils import *
from helper_files.cmdsLogger import PrintCaptureLogger
from colorama import Fore


def wc(**kwargs):
    print_capture_logger = PrintCaptureLogger()
    sys.stdout = print_capture_logger

    try:
        config = load_config()

        input = kwargs["input"] if kwargs.get("input") else []
        params = kwargs["params"] if kwargs.get("params") else []
        flags = kwargs["flags"] if kwargs.get("flags") else []

        try:
            is_line_count  = 'l' in flags
            is_word_count =  'w' in flags

            final_vlu = ""

            if params and input == []:
                for param in params:
                    param = param.replace("'", "").replace('"', "")
                    rd = read_file_data(param,config['cwdid'])

                    if rd["status_code"] == '200' and rd["data"] is not None:
                        counts = content_count(rd["data"], is_line_count, is_word_count)

                        parts = param.split("/")[-1]
                        final_vlu = final_vlu + "\n" +f"{' '.join(map(str,counts))} {parts}"

                    else:
                        print(f"{rd["message"]}")

                if final_vlu:
                    print(final_vlu)

            elif input and params == []:
                counts = content_count(input, is_line_count, is_word_count)
                final_vlu = ' '.join(map(str,counts))
                print(final_vlu)

        except Exception as e:
            print(Fore.RED+f"wc: {str(e)}")
    finally:
        sys.stdout = sys.__stdout__  # Restore the original stdout

    captured_output = "".join(print_capture_logger.log_content)
    return captured_output 
        


def content_count(data, isCountLine, isCountWord):
    char_count = len(data)
    line_count = len(data.splitlines()) if isCountLine else 0
    word_count = len(data.split()) if isCountWord else 0
    return [line_count, word_count, char_count]
