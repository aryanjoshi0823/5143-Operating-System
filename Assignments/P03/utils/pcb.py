class PCB:
    """
    PCB class represents a Process Control Block in the simulation.

    Attributes:
    - pid: Process ID.
    - priority: Priority level of the process.
    - arrivalTime: Time at which the process arrives in the system.
    - bursts: List of burst times required by the process.
    - currBurstType: Type of the current burst (e.g., 'CPU', 'IO').
    - currentBrust: Remaining time of the current burst.
    - CPUWaitTime: Time spent in the ready queue.
    - IOWaitTime: Time spent in the wait queue.
    - TurnAroundTime: Total time from start to finish for the process.
    - process_complete: Indicates whether the process has completed.
    - pendingBurst: List of burst times remaining to be processed.
    - terminate_back_count: Counter for terminating the process.
    - ready_cpu_wait: Time spent waiting in the ready queue for CPU.
    - wait_io_wait: Time spent waiting in the wait queue for IO.

    Methods:
    - __init__: Initializes the PCB with default values.
    - __str__: Returns a string representation of the PCB.
    - pending_brust: Updates the current burst and pending burst.
    - decrement_burst_time: Decrements the remaining time of the current burst.
    - get_current_burst_time: Returns the remaining time of the current burst.
    - released_process: Checks if the process has completed.
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
        self.process_complete = False
        self.ready_cpu_wait = 0
        self.wait_io_wait = 0
        self.priority_order = [f"p{i}" for i in range(1, 101)]

    def __str__(self):
        s = " "
        s += "".join(str(self.arrivalTime)) + " "
        s += "".join(str(self.pid)) + " "
        s += "".join(str(self.priority)) + " "
        s += "".join(str(self.currentBrust)) + " "
        s += "".join(str(self.bursts)) + " "
        s += "".join(str(self.pendingBurst)) + "\n"
        return s

    # def pending_brust(self):
    #     if len(self.pendingBurst) >= 1:
    #         self.currentBrust = self.pendingBurst[0]
    #         if len(self.pendingBurst) > 1:
    #             self.pendingBurst = self.pendingBurst[1:]
    #         else:
    #             self.pendingBurst = []

    #     else:
    #         self.pendingBurst = []
    #         self.currentBrust = 0

    def decrement_burst_time(self):
        self.currentBrust -= 1

    def get_current_burst_time(self):
        return self.currentBrust

    # def released_process(self): 
    #     if self.burst_types == "EXIT":
    #         self.process_complete = True
    #     return self.process_complete

    def setPriority(self):
        # (current_priority_index) * 2:
        current_priority_index = self.priority_order.index(self.priority) + 1
        if current_priority_index <= len(self.priority_order):
            if current_priority_index == 2:
                if self.CPUWaitTime_cpy >= 6:
                    self.priority = "p1"
                    self.CPUWaitTime_cpy = 0
            elif current_priority_index > 2:
                if self.CPUWaitTime_cpy >= (current_priority_index + 5) * 2:
                    self.priority = self.priority_order[current_priority_index - 2]
                    self.CPUWaitTime_cpy = 0