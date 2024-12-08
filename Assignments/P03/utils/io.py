class IO:
    """
    IO class represents an Input/Output device in the simulation.

    Attributes:
    - is_idle: Indicates whether the IO device is currently idle or serving a job.
    - current_job: Represents the job currently being served by the IO device.
    - total_execution_time: Represents the total execution time of the IO device.

    Methods:
    - __init__: Initializes the IO device with default values.
    - increment_execution_time: Increments the total execution time by 1.
    - load_job: Loads a job onto the IO device for processing.
    - complete_job: Checks if the current job is complete and returns it if so.
    - set_idle: Sets the IO device to idle state.
"""
    def __init__(self) -> None:
        self.is_idle = True
        self.current_job = None
        self.total_execution_time = 0

    def increment_execution_time(self):
        self.total_execution_time += 1

    def load_job(self, job):
        self.current_job = job
        self.is_idle = False

    def complete_job(self):
        if self.current_job.get_current_burst_time() == 0:
            completed_job = self.current_job
            return completed_job

    def set_idle(self):
        self.current_job = None
        self.is_idle = True