""" Effectively logging any messages passed to the write method. """ 

class CmdsLogger:
    def __init__(self):
        self.log_content = [] # To capture message.

    def write(self, msg):
        if msg:
            self.log_content.append(msg) # Appending message to above list.
