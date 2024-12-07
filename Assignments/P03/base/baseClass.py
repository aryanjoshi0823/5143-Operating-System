from utils.cpu import CPU
from utils.io import IO
from utils.pcb import PCB
from utils.api import *

from utils.queue import NewQueue, ReadyQueue, WaitQueue, TerminatedQueue
##from ui.ui_print import OverallStat
from datetime import datetime

import os

class BaseClass:
    """ 
        This class serve as base class for all the algorithm. All of the algorithm use this class for processing jobs. 
        This creates cups, ios etc required by the program
    """
    def __init__(self, cpu_Count, io_Count, time_Slice, algo_type):
        self.algo_type = algo_type
        self.time_Slice = time_Slice
        self.time_Slice_Copy = time_Slice
        self.cpu_Count = cpu_Count
        self.io_Count = io_Count
    
        self.new = NewQueue()
        self.wait = WaitQueue()
        self.ready = ReadyQueue()
        self.terminated = TerminatedQueue()
        current_time = str(datetime.now().strftime("%Y%m%d_%H%M%S"))

        self.client_id = "sgtrock"

        self.running = self.create_cpus()
        self.io = self.create_io()
        
        #self.readData()
        self.total_processes = self.new.length()

        self.terminated_process_count = 0
        self.total_tat = 0
        self.total_rwt = 0
        self.total_iwt = 0
        self.clock = 0
        self.session_id = 0
        self.message = []

        # 'a' appends to the file, create if not exists
        #file_name=algo_type+"_"+str(self.cpuCount)+"_"+str(self.ioCount)+"_"+self.datfile.split("/")[-1]

        self.header_written = False
        self.priority_req = False

        #self.message_file = self.open_file("message_"+file_name)
        #self.job_stats_file = self.open_file("job_stats_"+file_name)
        #self.overall_stats_file = self.open_file(  "overall_stats_"+file_name)


    def create_cpus(self):
        return [CPU() for _ in range(self.cpu_Count)]

    def create_io(self):
        return [IO() for _ in range(self.io_Count)]

    def __str__(self):
        s = ""
        s += "datfile: " + self.datfile + "\n"
        s += "new queue:\n" + "".join(str(pcb)
                                      for pcb in self.new.queue) + "\n"
        s += "wait:\n" + "".join(str(pcb) for pcb in self.wait.queue) + "\n"
        return s
    
    def time_increment(self):
        self.clock += 1

    def session_init(self):
        config = getConfig(self.client_id)
        response = init(config)
        self.clock = response['start_clock']
        self.session_id = response['session_id']
        
    def fetch_job(self):
        response = getJob(self.client_id, self.session_id, self.clock)
        if response and response['success']:
            for job in response['data']:
                job_id = job['job_id']
                self.new.addPCB(PCB(job["job_id"], [], [], job["arrival_time"], job["priority"]))  
                self.message.append(
                    f"[green]At time: {self.clock} [/green]job [bold gold1]pid_{job_id}[/bold gold1] [cyan]entered New queue[/cyan] \n")

    def move_new_ready(self):
        ready_processes = [process for process in self.new.queue if int(
            process.arrivalTime) + 1 <= self.clock]
        for process in ready_processes:
            self.message.append(
                f"[green]At time: {self.clock} [/green]job [bold gold1][pid_{process.pid}[/bold gold1] [bold green]{process.get_current_burst_time()}[/bold green]] [cyan]entered ready queue[/cyan] \n")
            self.ready.addPCB(process)
            self.new.queue.remove(process)
        if self.priority_req:
            self.ready.sort_by_priority()

    def ready_to_running(self):
        i = 1
        for cpu in self.running:
            # load one PCB to ech CPU from ready and remove from ready
            if cpu.is_idle and len(self.ready.queue):
                self.time_slice = self.time_Slice_Copy
                job = self.ready.removePCB()

                if not job.currentBrust:
                    burst = getBurst(self.client_id, self.session_id, job.pid)
                    if burst and burst['success']:
                        burst_type = burst['data']['burst_type']
                        burst_duration = int(burst['data']['duration'])

                        # Append burst info to the job
                        job.currentBrust = burst_duration
                        job.burst_types= burst_type

                        if burst_type == "CPU":
                            cpu.load_job(job)
                            self.message.append(
                                f"[green]At time: {self.clock} [/green]job [bold gold1][pid_{cpu.current_job.pid}[/bold gold1] [bold green]{cpu.current_job.get_current_burst_time()}[/bold green]] [cyan]obtained CPU_{i}[/cyan] \n")
                            
                        elif burst_type == "IO":
                            self.wait.addPCB(job)
                            self.message.append(
                            f"[green]At time: {self.clock} [/green]job [bold gold1][pid_{job.pid}[/bold gold1] [bold green]{job.get_current_burst_time()}[/bold green]] [cyan]entered Wait[/cyan] \n")

                        elif burst_type == "EXIT":
                            self.terminated.addPCB(job)
                            job.TurnAroundTime = self.clock - job.arrivalTime
                            self.terminated_process_count += 1
                            self.total_tat += job.TurnAroundTime
                            self.total_rwt += job.CPUWaitTime
                            self.total_iwt += job.IOWaitTime
                            self.message.append(
                                f"[green]At time: {self.clock} [/green]job [bold gold1][pid_{job.pid}[/bold gold1] [bold green]{job.get_current_burst_time()}[/bold green]] [cyan]entered Exit{i}[/cyan] \n")
                            

                else:
                    cpu.load_job(job)
                    self.message.append(
                        f"[green]At time: {self.clock} [/green]job [bold gold1][pid_{cpu.current_job.pid}[/bold gold1] [bold green]{cpu.current_job.get_current_burst_time()}[/bold green]] [cyan]obtained IO_{i}[/cyan] \n")

            i += 1

    def waiting_to_io(self):
        i = 1
        for io in self.io:
            if io.is_idle and len(self.wait.queue):
                wait_job = self.wait.removePCB()

                if not wait_job.currentBrust: 
                    burst = getBurst(self.client_id, self.session_id, wait_job.pid)
                    if burst and burst['success']:
                        burst_type = burst['data']['burst_type']
                        burst_duration = int(burst['data']['duration'])

                        # Append burst info to the job
                        wait_job.currentBrust = burst_duration
                        wait_job.burst_types= burst_type

                        if burst_type == "CPU":
                            self.ready.addPCB(wait_job)
                            self.message.append(
                            f"[green]At time: {self.clock} [/green]job [bold gold1][pid_{wait_job.pid}[/bold gold1] [bold green]{wait_job.get_current_burst_time()}[/bold green]] [cyan]entered Ready[/cyan] \n")

                
                        elif burst_type == "IO":
                            io.load_job(wait_job)
                            self.message.append(
                                f"[green]At time: {self.clock} [/green]job [bold gold1][pid_{io.current_job.pid}[/bold gold1] [bold green]{io.current_job.get_current_burst_time()}[/bold green]] [cyan]obtained IO_{i}[/cyan] \n")
                        
                        elif burst_type == "EXIT":
                            self.terminated.addPCB(wait_job)
                            wait_job.TurnAroundTime = self.clock - wait_job.arrivalTime
                            self.terminated_process_count += 1
                            self.total_tat += wait_job.TurnAroundTime
                            self.total_rwt += wait_job.CPUWaitTime
                            self.total_iwt += wait_job.IOWaitTime
                            self.message.append(
                                f"[green]At time: {self.clock} [/green]job [bold gold1][pid_{wait_job.pid}[/bold gold1] [bold green]{wait_job.get_current_burst_time()}[/bold green]] [cyan]entered Exit[/cyan] \n")
                            
                else:
                    io.load_job(wait_job)
                    self.message.append(
                        f"[green]At time: {self.clock} [/green]job [bold gold1][pid_{io.current_job.pid}[/bold gold1] [bold green]{io.current_job.get_current_burst_time()}[/bold green]] [cyan]obtained IO_{i}[/cyan] \n")

            i += 1

    def prevent_starvation(self):
        for process in self.ready.queue:
            if (self.clock - process.arrivalTime) > self.starvation_threshold:
                self.message.append(
                    f"[yellow]Job [pid_{process.pid}] promoted to higher priority due to long wait[/yellow]"
                )
                process.priority -= 1  # Promote priority (lower value = higher priority).

    def preempt_if_necessary(self):
        for cpu in self.running:
            if not cpu.is_idle:
                # Check if the current job has lower priority than any in the ready queue
                highest_priority_job = self.ready.queue[0]
                if highest_priority_job.priority < cpu.current_job.priority:
                    # Preempt current job
                    self.ready.addPCB(cpu.current_job)
                    self.message.append(
                        f"[red]Job [pid_{cpu.current_job.pid}] preempted by [pid_{highest_priority_job.pid}][/red]"
                    )
                    cpu.set_idle()