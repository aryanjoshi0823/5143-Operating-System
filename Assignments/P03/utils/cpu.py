class CPU:
    """
    CPU class represents the central processing unit in the simulation.

    Attributes:
    - is_idle: Indicates whether the CPU is currently idle or processing a job.
    - current_job: Represents the job currently being processed.
    - total_execution_time: Represents the total execution time of the CPU.

    Methods:
    - __init__: Initializes the CPU with default values.
    - __str__: Returns a string representation of the CPU.
    - increment_execution_time: Increments the total execution time by 1.
    - load_job: Loads a job onto the CPU for processing.
    - complete_job: Checks if the current job is complete and returns it if so.
    - set_idle: Sets the CPU to idle state.
"""
    def __init__(self):
        self.is_idle = True
        self.current_job = None
        self.total_execution_time = 0

    def __str__(self):
        s = ""
        s += self.complete_job + " "
        return s

    def increment_execution_time(self):
        self.total_execution_time += 1

    def load_job(self, job):
        self.current_job = job
        self.is_idle = False

    def complete_job(self):
        if self.current_job.get_current_burst_time() == 0:
            completed_job = self.current_job
            # self.set_idle()
            return completed_job

    def set_idle(self):
        self.current_job = None
        self.is_idle = True