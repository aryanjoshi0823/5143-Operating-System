def echo(**kwargs):
    if "params" in kwargs:
        params = kwargs["params"] if kwargs.get("params") else []
        input = kwargs["input"] if kwargs.get("input") else []

    def remove_outer_quotes(param):
        # Check if the string starts and ends with the same quote (either ' or ")
        if (param.startswith('"') and param.endswith('"')) or (param.startswith("'") and param.endswith("'")):
            return param[1:-1]  # Remove the outermost quotes
        return param # Return as is if no outer quotes
    
    if params:
        cleaned_params = " ".join([remove_outer_quotes(p) for p in params]) 
        print(cleaned_params)
    else:
        cleaned_params = "".join([remove_outer_quotes(p) for p in input]) 
        print(cleaned_params)
    return (str(cleaned_params))
