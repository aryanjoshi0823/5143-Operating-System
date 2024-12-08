from utils.api import *
from base.baseClass import BaseClass
from utils.rich_print import UI_Layout
from rich.live import Live
import time

class PriorityBased(BaseClass):

    def __init__(self, cpu_count, io_count, time_slice, algorithm_type, speed, starvation_threshold=10):  
        super().__init__(cpu_count, io_count, time_slice, algorithm_type)
        self.speed = speed
        self.starvation_threshold = starvation_threshold  # Time threshold to promote low-priority processes.

    def run_algorithm(self):
        self.session_init()
        with Live(
            UI_Layout(
                self.new.queue,
                self.ready.queue,
                self.running,
                self.wait.queue,
                self.io,
                self.terminated.queue,
                self.clock,
                self.message,
                self.total_processes,
                self.terminated_process_count,
                self.cpu_Count,
                self.io_Count,
                self.algo_type
            ),
            refresh_per_second=10,
        ) as live:

            while True:
                time.sleep(self.speed)
                self.message = []
                jobs_left = getJobsLeft(self.client_id, self.session_id)
                if jobs_left == 0:
                    break

                # Fetch new jobs
                self.fetch_job()

                # Move new processes to ready queue
                self.move_new_ready()
                self.ready.increment_CPUWaitTime()

                # Check and promote processes to prevent starvation
                #self.prevent_starvation()

                # Sort the ready queue by priority (lower number = higher priority)
                self.ready.queue.sort(key=lambda job: job.priority)

                if len(self.ready.queue) > 0:
                    self.preempt_if_necessary()
                    self.ready_to_running()

                i = 1
                for cpu in self.running:
                    if not cpu.is_idle:
                        cpu.increment_execution_time()
                        cpu.current_job.decrement_burst_time()
                        self.message.append(
                            f"[green]At time: {self.clock} [/green]job [bold gold1][pid_{cpu.current_job.pid}[/bold gold1] [bold green]{cpu.current_job.get_current_burst_time()}[/bold green]] [cyan]is running in CPU_{i}[/cyan] \n")
                        
                        complete_job = cpu.complete_job()
                        if complete_job:
                            self.wait.addPCB(complete_job)
                            self.wait.increment_IOWaitTime()
                            self.message.append(
                                f"[green]At time: {self.clock} [/green]job [bold gold1][pid_{complete_job.pid}[/bold gold1] [bold green]{complete_job.get_current_burst_time()}[/bold green]] [cyan]entered wait queue[/cyan] \n")
                            cpu.set_idle()

                    i += 1

                if len(self.wait.queue) > 0:
                    self.waiting_to_io()

                j = 1 
                for io in self.io:
                    if not io.is_idle:
                        io.increment_execution_time()
                        io.current_job.decrement_burst_time()
                        self.message.append(
                            f"[green]At time: {self.clock} [/green]job [bold gold1][pid_{io.current_job.pid}[/bold gold1] [bold green]{io.current_job.get_current_burst_time()}[/bold green]] [cyan]is running in IO_{j}[/cyan] \n")
                        complete_job = io.complete_job()
                        if complete_job:
                            self.ready.addPCB(complete_job)
                            self.message.append(
                                f"[green]At time: {self.clock} [/green]job [bold gold1][pid_{complete_job.pid}[/bold gold1] {complete_job.get_current_burst_time()}]  [red]IO completed and entered ready queue[/red] \n")
                            io.set_idle()
                    j += 1

                # Update live display
                self.clock += 1
                live.update(
                    UI_Layout(
                        self.new.queue,
                        self.ready.queue,
                        self.running,
                        self.wait.queue,
                        self.io,
                        self.terminated.queue,
                        self.clock,
                        self.message,
                        self.total_processes,
                        self.terminated_process_count,
                        self.cpu_Count,
                        self.io_Count,
                        self.algo_type
                    )
                )


