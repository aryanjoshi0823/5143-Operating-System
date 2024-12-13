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
    def __init__(self, cpu_Count, io_Count, time_Slice, algo_type, speed = 0, mlfq_levels = 3):
        self.algo_type = algo_type
        self.time_Slice = time_Slice
        self.time_Slice_Copy = time_Slice
        self.cpu_Count = cpu_Count
        self.io_Count = io_Count
        self.speed = speed
        self.mlfq_levels = mlfq_levels
    
        self.new = NewQueue()
        self.wait = WaitQueue()
        self.ready = ReadyQueue()
        self.terminated = TerminatedQueue()

        self.client_id = "sgtrock"

        self.running = self.create_cpus()
        self.io = self.create_io()
        self.total_processes = self.ready.length()


        self.terminated_process_count = 0
        self.total_tat = 0
        self.total_rwt = 0
        self.total_iwt = 0
        self.clock = 0
        self.session_id = 0

        self.message = []

        self.cycle_count = 0
        self.toggle_priority_adjustment = False 


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
                if job_id:
                    burst = getBurst(self.client_id, self.session_id, job_id)
                    if burst and burst['success']:
                        burst_type = burst['data']['burst_type']
                        burst_duration = int(burst['data']['duration'])
                        self.new.addPCB(PCB(job["job_id"], burst_duration, burst_type, job["arrival_time"], job["priority"]))  
                        self.message.append(
                            f"[green]At time: {self.clock} [/green]job [bold gold1]pid_{job_id}[/bold gold1] [cyan]entered New queue[/cyan] \n")

    def move_new_ready(self):
        ready_processes = [process for process in self.new.queue if int(process.arrivalTime) + 1 <= self.clock]
        for process in ready_processes:
            self.message.append(
                f"[green]At time: {self.clock} [/green]job [bold gold1][pid_{process.pid}[/bold gold1] [bold green]{process.get_current_burst_time()}[/bold green]] [cyan]entered ready queue[/cyan] \n")
            self.ready.addPCB(process)
            self.new.queue.remove(process)

    def move_new_ready_mlfq(self):
        ready_processes = [process for process in self.new.queue if int(process.arrivalTime) + 1 <= self.clock]
        for process in ready_processes:
            burst_time = process.currentBrust

            # Dynamically find the appropriate queue based on burst time
            for index, queue_info in enumerate(self.ready.queue):
                if burst_time <= queue_info["quantum"]:
                    queue_info['queue'].append(process)
                    print(f"Process {process.pid} moved to Queue {index + 1} (Priority {queue_info['priority']})")
                    break  
                
            self.new.queue.remove(process)

    def ready_to_running(self):
        i = 1
        for cpu in self.running:
            # load one PCB to ech CPU from ready and remove from ready
            if cpu.is_idle and len(self.ready.queue):
                self.time_slice = self.time_Slice_Copy
                job = self.ready.removePCB()

                if job.burst_types == "CPU":
                    cpu.load_job(job)
                    # self.message.append(
                    #     f"[green]At time: {self.clock} [/green]job [bold gold1][pid_{cpu.current_job.pid}[/bold gold1] [bold green]{cpu.current_job.get_current_burst_time()}[/bold green]] [cyan]obtained CPU_{i}[/cyan] \n")

            i += 1

    def waiting_to_io(self):
        i = 1
        for io in self.io:
            if io.is_idle and len(self.wait.queue):
                wait_job = self.wait.removePCB()
                if wait_job.burst_types == "IO":
                    io.load_job(wait_job)
            i += 1

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