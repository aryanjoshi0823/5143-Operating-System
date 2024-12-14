from utils.api import *
from base.baseClass import BaseClass
from utils.rich_print_mlfq import UI_Layout,OverallStat
from rich.live import Live
from utils.queue import ReadyQueue
from collections import deque
import time

class MLFQ(BaseClass):
    def __init__(self, cpu_count, io_count, time_slice, algorithm_type, speed, mlfq_levels = 3):  
        super().__init__(cpu_count, io_count, time_slice, algorithm_type, speed,mlfq_levels)

        if len(self.time_Slice) != self.mlfq_levels:
            raise ValueError("The length of time slice must match the number of levels")
        
        self.ready.queue = [
            {'queue': deque(), 'quantum': self.time_Slice[i], 'priority': i + 1}
            for i in range(self.mlfq_levels)
        ]

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

                self.fetch_job()
                self.move_new_ready_mlfq()
                self.ready.increment_CPUWaitTime_mlfq()
                self.handle_starvation()
                self.ready_to_running_mlfq()

                i = 1          
                for cpu in self.running:
                    if not cpu.is_idle:
                        cpu.increment_execution_time() 
                        if self.clock_tick_count <= cpu.current_job.queue_time_slice:
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

                                    self.clock_tick_count = 0

                                    if burst_type == "CPU":
                                        inserted_cpu_ready= False
                                
                                        for index, queue_info in enumerate(self.ready.queue):
                                            if complete_job.currentBrust <= queue_info["quantum"]:
                                                complete_job.queue_time_slice = queue_info["quantum"]
                                                queue_info['queue'].append(complete_job)
                                                self.ready.increment_CPUWaitTime_mlfq()
                                                self.message.append(
                                                    f"[green]At time: {self.clock} [/green]job [bold gold1][pid_{complete_job.pid}[/bold gold1] [bold green]{complete_job.get_current_burst_time()}[/bold green]] [cyan]entered ready queue {index + 1}[/cyan] \n")
                                                inserted_cpu_ready = True
                                                break 

                                        # If no matching queue was found, insert the job into the last priority queue
                                        if not inserted_cpu_ready:
                                            complete_job.queue_time_slice = self.ready.queue[-1]["quantum"]
                                            self.ready.queue[-1]['queue'].append(complete_job)
                                            self.ready.increment_CPUWaitTime_mlfq()
                                            self.message.append(
                                                f"[green]At time: {self.clock} [/green]job [bold gold1][pid_{complete_job.pid}[/bold gold1] [bold green]{complete_job.get_current_burst_time()}[/bold green]] [cyan]entered ready queue (default to last level)[/cyan] \n")
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
                                        cpu.set_idle()

                        else:
                            # If not finished, increase waiting time of others and demote job to next queue
                            for index, queue_info in enumerate(self.ready.queue):
                                if index + 1 < len(self.ready.queue):
                                    self.ready.queue[index + 1]['queue'].append(cpu.current_job)
                                    self.ready.increment_CPUWaitTime_mlfq()
                                    self.message.append(
                                        f"[green]At time: {self.clock} [/green]job [bold gold1][pid_{cpu.current_job.pid}[/bold gold1] [bold green]{cpu.current_job.get_current_burst_time()}[/bold green]] [cyan]entered ready queue {index + 1}[/cyan] \n")
                                    break 
                                else:
                                    queue_info['queue'].append(cpu.current_job)
                                    self.ready.increment_CPUWaitTime_mlfq()

                            self.clock_tick_count = 0
                            cpu.set_idle() 
                        i+=1


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
                                    inserted_io_ready= False
                                    for index, queue_info in enumerate(self.ready.queue):
                                        if complete_job.currentBrust <= queue_info["quantum"]:
                                            complete_job.queue_time_slice = queue_info["quantum"]
                                            queue_info['queue'].append(complete_job)
                                            self.ready.increment_CPUWaitTime_mlfq()
                                            self.message.append(
                                                f"[green]At time: {self.clock} [/green]job [bold gold1][pid_{complete_job.pid}[/bold gold1] [bold green]{complete_job.get_current_burst_time()}[/bold green]] [cyan]entered ready queue {index + 1}[/cyan] \n")
                                            inserted_io_ready = True
                                            break 

                                    # If no matching queue was found, insert the job into the last priority queue
                                    if not inserted_io_ready:
                                        complete_job.queue_time_slice = self.ready.queue[-1]["quantum"]
                                        self.ready.queue[-1]['queue'].append(complete_job)
                                        self.ready.increment_CPUWaitTime_mlfq()
                                        self.message.append(
                                            f"from not inserted queue [green]At time: {self.clock} [/green]job [bold gold1][pid_{complete_job.pid}[/bold gold1] [bold green]{complete_job.get_current_burst_time()}[/bold green]] [cyan]entered ready queue (default to last level)[/cyan] \n")

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

                self.clock += 1
                self.clock_tick_count +=1
                self.total_simulation_time +=1
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
        
        ATAT, ARWT, AIWT, cpu_util, io_util = self.calculate_overall_statistics()

        overall_stats = OverallStat(ATAT, ARWT, AIWT, cpu_util, io_util)
        overall_stats.display_table()
                