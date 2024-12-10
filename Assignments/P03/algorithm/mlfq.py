from utils.api import *
from base.baseClass import BaseClass
from utils.rich_print import UI_Layout
from rich.live import Live
from utils.queue import ReadyQueue
import time

class MLFQ(BaseClass):
    def __init__(self, cpu_count, io_count, time_slice, algorithm_type, speed):  
        super().__init__(cpu_count, io_count, time_slice, algorithm_type)
        self.speed = speed
        self.queues = [
            {'queue': ReadyQueue(), 'quantum': 4},
            {'queue': ReadyQueue(), 'quantum': 8},
            {'queue': ReadyQueue(), 'quantum': 16}
        ]
        self.aging_threshold = 20

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

                # Fetch and move new jobs to the highest-priority queue
                self.fetch_job()
                self.move_new_ready()
                self.queues[0]['queue'].extend(self.ready.queue)
                self.ready.emptyq()

                for queue_data in self.queues:
                    queue = queue_data['queue']
                    quantum = queue_data['quantum']

                    if queue.length() > 0:
                        job = queue.removePCB()

                        # Run job for its quantum or remaining burst time
                        execution_time = min(job.get_current_burst_time(), quantum)
                        job.decrement_burst_time()
                        self.clock += execution_time
                        job.CPUWaitTime += execution_time
                        job.CPUWaitTime_cpy += execution_time
                        self.message.append(
                            f"[green]At time: {self.clock} [/green]job [bold gold1][pid_{job.pid}[/bold gold1] [bold green]{job.get_current_burst_time()}[/bold green]] [cyan]ran for {execution_time} ms in Queue with Quantum {quantum}[/cyan] \n"
                        )

                        # Check job state
                        if job.get_current_burst_time() <= 0:
                            self.terminated.addPCB(job)
                            self.terminated_process_count += 1
                            self.message.append(
                                f"[green]Job {job.pid} completed and moved to terminated queue[/green]\n"
                            )
                        else:
                            next_queue_index = self.queues.index(queue_data) + 1
                            if next_queue_index < len(self.queues):
                                self.queues[next_queue_index]['queue'].addPCB(job)
                                self.message.append(
                                    f"[yellow]Job {job.pid} moved to lower-priority queue[/yellow]\n"
                                )
                            else:
                                queue.addPCB(job)  # Stay in the same queue if it's the lowest

                # Implement aging for lower-priority jobs
                for lower_queue_data in self.queues[1:]:
                    for job in lower_queue_data['queue'].queue:
                        job.CPUWaitTime += execution_time
                        if job.CPUWaitTime >= self.aging_threshold:
                            lower_queue_data['queue'].queue.remove(job)
                            self.queues[0]['queue'].addPCB(job)
                            job.CPUWaitTime = 0
                            self.message.append(
                                f"[yellow]Job {job.pid} promoted due to aging[/yellow]\n"
                            )

                # Update live display
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
