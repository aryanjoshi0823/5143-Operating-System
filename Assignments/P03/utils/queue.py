from rich import print
import time

class Queue:
    """
    Queue class represents a basic First-In-First-Out (FIFO) data structure for managing Process Control Blocks (PCBs).

    Attributes:
    - queue: A list to store PCB objects in the order they are added.

    Methods:
    - __init__: Initializes an empty queue.
    - __str__: Converts the queue elements to a string for easy printing.
    - addPCB(pcb): Adds a Process Control Block (PCB) to the end of the queue.
    - removePCB(): Removes and returns the first PCB from the queue (FIFO).
    - length(): Returns the number of PCBs in the queue.
    - extend(lst): Extends the queue by appending PCBs from a list.
    - emptyq(): Clears the queue, making it empty.
    - sort_by_priority(): Sorts the PCB objects in the queue based on their priority.
    - returnPriority(): Returns the priority of the first PCB in the queue, or a default priority if the queue is empty.
"""
    def __init__(self):
        self.queue = []

    def addPCB(self, pcb):
        
        """
        Add a new PCB to the queue if it doesn't already exist.
        """  
        self.queue.append(pcb)

    def removePCB(self):
       return self.queue.pop(0) if self.queue else None

    def length(self):
        return len(self.queue)

    def extend(self, lst):
        self.queue.extend(lst)

    def emptyq(self):
        self.queue = []
    
    def get_pcb_by_id(self, pid):
        """
        Retrieve a PCB by job ID.
        """
        for pcb in self.queue:
            if pcb.pid == pid:
                return pcb
        return None

    def sort_by_priority(self):
        # Sort the PCB objects in the queue based on their priority
        self.queue.sort(key=lambda pcb: pcb.priority)

    def returnPriority(self):
        if len(self.queue) > 0:
            return self.queue[0].priority[1]
        else:
            return 10


class NewQueue(Queue):
    """ Holds processes waiting for IO device
    """

    def __init__(self):
        super().__init__()


class ReadyQueue(Queue):
    """ Holds processes ready to run on cpu
    """

    def __init__(self):
        super().__init__()

    def increment_CPUWaitTime(self):
        for p in self.queue:
            p.CPUWaitTime += 1
            p.CPUWaitTime_cpy += 1

    def increment_CPUWaitTime_mlfq(self):
        for index, queue_info in enumerate(self.queue):
            for p in queue_info['queue']:
                p.CPUWaitTime += 1
                p.CPUWaitTime_cpy += 1




class WaitQueue(Queue):
    """ Holds processes waiting for IO device
    """

    def __init__(self):
        super().__init__()

    def increment_IOWaitTime(self):
        for p in self.queue:
            p.IOWaitTime += 1


class TerminatedQueue(Queue):
    """ Holds  completed jobs
    """

    def __init__(self):
        super().__init__()



