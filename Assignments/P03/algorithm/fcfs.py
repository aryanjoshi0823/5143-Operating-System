from utils.api import *
from base.baseClass import BaseClass
from utils.rich_print import UI_Layout
from rich.live import Live
import time

class FCFS(BaseClass):

    def __init__(self, cpu_count, io_count, time_slice, algorithm_type, speed):  
        super().__init__(cpu_count, io_count, time_slice, algorithm_type)

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
                jobs_left = getJobsLeft(self.client_id,self.session_id)
                if jobs_left == 0:
                    break

                # Get new jobs for the current clock
                self.fetch_job()

                self.move_new_ready()
                self.ready.increment_CPUWaitTime()

                if len(self.ready.queue) > 0:
                    self.ready_to_running()

                i = 1          
                for cpu in self.running:
                    if not cpu.is_idle:
                        """ get current CPU brust 
                            Decrement time for that brust 
                            Add excution time for cal runninng time
                            check time_silce :   "Job {cpu.runningPCB.pid}: preempted"")
                            and move to ready stat 
                            if all brust compelted so move to terminate 
                            else run wait and IO
                        """
                        cpu.increment_execution_time()
                        cpu.current_job.decrement_burst_time()
                        self.message.append(
                            f"[green]At time: {self.clock} [/green]job [bold gold1][pid_{cpu.current_job.pid}[/bold gold1] [bold green]{cpu.current_job.get_current_burst_time()}[/bold green]] [cyan]is running in CPU_{i}[/cyan] \n")
                        
                        complete_job = cpu.complete_job()
                        if complete_job:

                            burst = getBurst(self.client_id, self.session_id, complete_job.pid)
                            if burst and burst['success']:
                                burst_type = burst['data']['burst_type']
                                burst_duration = int(burst['data']['duration'])

                                # Append burst info to the job
                                complete_job.currentBrust = burst_duration
                                complete_job.burst_types= burst_type

                                if burst_type == "CPU":
                                    self.ready.addPCB(complete_job)
                                    self.ready.increment_CPUWaitTime()
                                    self.message.append(
                                        f"[green]At time: {self.clock} [/green]job [bold gold1][pid_{complete_job.pid}[/bold gold1] [bold green]{complete_job.get_current_burst_time()}[/bold green]] [cyan]entered Ready[/cyan] \n")
                                    cpu.set_idle()

                                elif burst_type == "IO":
                                    self.wait.addPCB(complete_job)
                                    self.wait.increment_IOWaitTime()
                                    self.message.append(
                                    f"[green]At time: {self.clock} [/green]job [bold gold1][pid_{complete_job.pid}[/bold gold1] [bold green]{complete_job.get_current_burst_time()}[/bold green]] [cyan]entered Wait queue[/cyan] \n")
                                    cpu.set_idle()

                                elif burst_type == "EXIT":
                                    self.terminated.addPCB(complete_job)
                                    complete_job.TurnAroundTime = self.clock - complete_job.arrivalTime
                                    self.terminated_process_count += 1
                                    self.total_tat += complete_job.TurnAroundTime
                                    self.total_rwt += complete_job.CPUWaitTime
                                    self.total_iwt += complete_job.IOWaitTime
                                    self.message.append(
                                        f"[green]At time: {self.clock} [/green]job [bold gold1][pid_{complete_job.pid}[/bold gold1] [bold green]{complete_job.get_current_burst_time()}[/bold green]] [cyan]entered Exit queue{i}[/cyan] \n")
                                    # self.write_stat(
                                    #     (f'{complete_job.pid},{complete_job.arrivalTime},{complete_job.TurnAroundTime},{complete_job.CPUWaitTime},{complete_job.IOWaitTime}\n'))
                                    cpu.set_idle()
                    i += 1

                if (len(self.wait.queue) > 0):
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

                            burst = getBurst(self.client_id, self.session_id, complete_job.pid)
                            if burst and burst['success']:
                                burst_type = burst['data']['burst_type']
                                burst_duration = int(burst['data']['duration'])

                                # Append burst info to the job
                                complete_job.currentBrust = burst_duration
                                complete_job.burst_types= burst_type

                                if burst_type == "CPU":
                                    self.ready.addPCB(complete_job)
                                    self.ready.increment_CPUWaitTime()
                                    self.message.append(
                                    f"[green]At time: {self.clock} [/green]job [bold gold1][pid_{complete_job.pid}[/bold gold1] [bold green]{complete_job.get_current_burst_time()}[/bold green]] [cyan]entered Ready queue[/cyan] \n")
                                    io.set_idle()

                                elif burst_type == "IO":
                                    self.wait.addPCB(complete_job)
                                    self.wait.increment_IOWaitTime()
                                    self.message.append(
                                        f"[green]At time: {self.clock} [/green]job [bold gold1][pid_{complete_job.pid}[/bold gold1] [bold green]{complete_job.get_current_burst_time()}[/bold green]] [cyan]entered Wait queue[/cyan] \n")
                                    io.set_idle()
                                
                                elif burst_type == "EXIT":
                                    self.terminated.addPCB(complete_job)
                                    complete_job.TurnAroundTime = self.clock - complete_job.arrivalTime
                                    self.terminated_process_count += 1
                                    self.total_tat += complete_job.TurnAroundTime
                                    self.total_rwt += complete_job.CPUWaitTime
                                    self.total_iwt += complete_job.IOWaitTime
                                    self.message.append(
                                        f"[green]At time: {self.clock} [/green]job [bold gold1][pid_{complete_job.pid}[/bold gold1] [bold green]{complete_job.get_current_burst_time()}[/bold green]] [cyan]entered Exit[/cyan] \n")
                                    io.set_idle()
                    j += 1

                #Update live display
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






        

