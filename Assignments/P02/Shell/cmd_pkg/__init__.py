from .pwd import pwd
from .ls import ls
from .echo import echo
from .grep import grep
from .history import history
from .whoami import whoami 
from .filesCommands import *
from .exit import exit
from .clear import clear
from .getch import Getch


__all__ = [
    "pwd", 
    "ls", 
    "echo", 
    "grep", 
    "add_commands_to_history",
    "whoami",
    "history", 
    "filesCommands", 
    "exit"
    "cat",
    "head",
    "Getch",
    "clear"
]
