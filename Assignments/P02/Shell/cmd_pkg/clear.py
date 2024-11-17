
def clear(**kwargs):
    """Clears the terminal and moves the prompt to the top-left corner."""

    # use \033[H to move the cursor to the home position (top-left corner of the terminal) 
    # and then clear the screen with \033[J. This effectively simulates clearing the 
    # terminal and repositioning the prompt.
    print("\033[H\033[J", end="") 
    return ""