from helper_files.api_call import *
from helper_files.utils import *

def wc(**kwargs):

    config = load_config()

    input = kwargs["input"] if kwargs.get("input") else []
    params = kwargs["params"] if kwargs.get("params") else []
    flags = kwargs["flags"] if kwargs.get("flags") else []

    print("input in wc---->",input)

    try:
        is_line_count  = 'l' in flags
        is_word_count =  'w' in flags

        final_vlu = ""
        if params:
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
                return (str(final_vlu))
        else:
            counts = content_count(input, is_line_count, is_word_count)
            final_vlu = ' '.join(map(str,counts))
            print(final_vlu)
            return (str(final_vlu))

    except Exception as e:
        print(f"Error: {str(e)}")
        


def content_count(data, isCountLine, isCountWord):
    char_count = len(data)
    line_count = len(data.splitlines()) if isCountLine else 0
    word_count = len(data.split()) if isCountWord else 0
    return [line_count, word_count, char_count]
