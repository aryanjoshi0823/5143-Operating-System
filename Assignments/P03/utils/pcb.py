class PCB:
    """
    PCB class represents a Process Control Block in the simulation.

    Attributes:
    - pid: Process ID.
    - priority: Priority level of the process.
    - arrivalTime: Time at which the process arrives in the system.
    - bursts: List of burst times required by the process.
    - burst_types: Type of the current burst (e.g., 'CPU', 'IO').
    - currentBrust: Remaining time of the current burst.
    - CPUWaitTime: Time spent in the ready queue.
    - IOWaitTime: Time spent in the wait queue.
    - TurnAroundTime: Total time from start to finish for the process.

    Methods:
    - __init__: Initializes the PCB with default values.
    - pending_brust: Updates the current burst and pending burst.
    - decrement_burst_time: Decrements the remaining time of the current burst.
    - get_current_burst_time: Returns the remaining time of the current burst.
    - setPriority: Adjusts the priority of the process based on waiting times.
"""
    def __init__(self, jid, burst, burst_type,  arrival_t, priority):
        self.pid = jid
        self.priority = priority
        self.arrivalTime = int(arrival_t)
        self.burst_types = burst_type
        self.currentBrust = burst
        self.CPUWaitTime = 0
        self.CPUWaitTime_cpy = 0      # Time in ready queue
        self.IOWaitTime = 0           # Time in wait queue
        self.TurnAroundTime = 0       # Time from start to finish
        self.queue_time_slice = 0 
        self.starvation_counter = 0 



    def decrement_burst_time(self):
        self.currentBrust -= 1

    def get_current_burst_time(self):
        return self.currentBrust

