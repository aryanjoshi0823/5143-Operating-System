from utils.cpu import CPU
from utils.io import IO
from utils.pcb import PCB
from utils.api import *

from utils.queue import NewQueue, ReadyQueue, WaitQueue, TerminatedQueue
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

        self.total_simulation_time = 0
        self.total_processes = 0
        self.clock_tick_count = 0
        self.terminated_process_count = 0
        self.total_tat = 0
        self.total_rwt = 0
        self.total_iwt = 0
        self.clock = 0
        self.session_id = 0

        self.message = []


    def create_cpus(self):
        return [CPU() for _ in range(self.cpu_Count)]

    def create_io(self):
        return [IO() for _ in range(self.io_Count)]

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
                        self.total_processes += 1
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
            inserted = False

            # Dynamically find the appropriate queue based on burst time
            for index, queue_info in enumerate(self.ready.queue):
                if burst_time <= queue_info["quantum"]:
                    process.queue_time_slice = queue_info["quantum"]
                    queue_info['queue'].append(process)
                    self.message.append(
                        f"[green]At time: {self.clock} [/green]job [bold gold1][pid_{process.pid}[/bold gold1] [bold green]{process.get_current_burst_time()}[/bold green]] [cyan]entered ready queue {index + 1}[/cyan] \n")
                    inserted = True
                    break 

            # If no matching queue was found, insert the job into the last priority queue
            if not inserted:
                self.ready.queue[-1]['queue'].append(process)
                process.queue_time_slice = self.ready.queue[-1]["quantum"]
                self.message.append(
                    f"[green]At time: {self.clock} [/green]job [bold gold1][pid_{process.pid}[/bold gold1] [bold green]{process.get_current_burst_time()}[/bold green]] [cyan]entered ready queue (default to last level)[/cyan] \n")

            self.new.queue.remove(process)
        
    def ready_to_running_mlfq(self):
        i = 1
        for cpu in self.running:
            if cpu.is_idle:
                # load one PCB to ech CPU from ready and remove from ready
                for index, queue_info in enumerate(self.ready.queue):
                    if queue_info['queue']:
                        job = queue_info['queue'].popleft()
                        if job.burst_types == "CPU":
                            job.starvation_counter = 0 
                            cpu.load_job(job)
                            self.message.append(
                                f"[green]At time: {self.clock} [/green]job [bold gold1][pid_{cpu.current_job.pid}[/bold gold1] [bold green]{cpu.current_job.get_current_burst_time()}[/bold green]] [cyan]obtained ready cpu_{i}[/cyan] \n")
                        break  
            i += 1

    def ready_to_running(self):
        i = 1
        for cpu in self.running:
            # load one PCB to ech CPU from ready and remove from ready
            if cpu.is_idle and len(self.ready.queue):
                self.time_slice = self.time_Slice_Copy
                job = self.ready.removePCB()

                if job.burst_types == "CPU":
                    cpu.load_job(job)
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

    def calculate_overall_statistics(self):
        """Calculate and return overall statistics at the end of the simulation."""
        # Calculate metrics
        simulation_time = self.total_simulation_time
        terminated_queue = self.terminated
        cpus = self.running
        ios = self.io

        total_tat = sum(job.TurnAroundTime for job in terminated_queue.queue)
        total_rwt = sum(job.CPUWaitTime for job in terminated_queue.queue)
        total_iwt = sum(job.IOWaitTime for job in terminated_queue.queue)
        num_processes = len(terminated_queue.queue)
        print("num_processes-->",num_processes)
        print("sim time -->",simulation_time)

        total_cpu_busy_time = sum(cpu.total_execution_time for cpu in cpus)
        total_io_busy_time = sum(io.total_execution_time for io in ios)
        print("total_cpu_busy_time-->",total_cpu_busy_time)
        print("total_io_busy_time-->",total_io_busy_time)

        ATAT = total_tat / num_processes if num_processes > 0 else 0
        ARWT = total_rwt / num_processes if num_processes > 0 else 0
        AIWT = total_iwt / num_processes if num_processes > 0 else 0
        cpu_utilization = (total_cpu_busy_time / simulation_time) * 100 if simulation_time > 0 else 0
        io_utilization = (total_io_busy_time / simulation_time) * 100 if simulation_time > 0 else 0

        # Return metrics
        return ATAT, ARWT, AIWT, cpu_utilization, io_utilization

    def handle_starvation(self):
        """
        Checks for starvation in the lower-priority queues and promotes jobs with starvation_counter > 20.
        """
        for i in range(1, len(self.ready.queue)):  # Start from the second queue (index 1)
            queue_info = self.ready.queue[i]
            for job in list(queue_info['queue']):  
                if job.starvation_counter > 20:  

                    queue_info['queue'].remove(job)
                    job.starvation_counter = 0  

                    # Promote the job to the higher-priority queue
                    self.ready.queue[i - 1]['queue'].append(job)
                    job.queue_time_slice = self.ready.queue[i - 1]['quantum']  # Update time slice
                    self.message.append(
                        f"[green]At time: {self.clock}[/green]job [bold gold1][pid_{job.pid}[/bold gold1][bold green]{job.get_current_burst_time()}[/bold green]] [cyan]promoted to queue {i}[/cyan] \n"
                    )
 

