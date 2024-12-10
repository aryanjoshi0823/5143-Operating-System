from rich import print
from rich.table import Table
from rich.text import Text
from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.style import Style

# [bold gold1]
# [bold blue]
class QueueTable:
    def __init__(self, new, ready, running, wait, io, terminate, messages) -> None:
        # Initializes the QueueTable with process queues and a console for displaying output.
        self.console = Console()
        self.terminal_width = self.console.width
        self.new = new
        self.ready = ready
        self.running = running
        self.wait = wait
        self.io = io
        self.terminate = terminate
        self.message = messages

    def make_row(self, queueName, queue_list, flag=False):
        # Creates a single row for the table showing process details for a given queue.
        processes = ""
        if flag:
            for cpu_io in queue_list:
                if cpu_io.current_job:
                    processes += str(
                        f"[bold gold1] [white][ [/white]Pid_{cpu_io.current_job.pid}[/bold gold1] [bold green] [bold green]{cpu_io.current_job.currentBrust}[/bold green] [bold blue] {cpu_io.current_job.priority} [white]][/white][/bold blue][/bold green]")
        else:
            for pcb in queue_list:
                processes += str(
                    f"[bold gold1] [white][ [/white]Pid_{pcb.pid}[/bold gold1] [bold green] {pcb.currentBrust} [bold blue] {pcb.priority} [white]][/white][/bold blue][/bold green]")
        return [queueName, processes]

    def generate_table(self):
        # Generates the main table displaying all queues and their processes.
        table = Table(show_header=False)
        table.add_column("Queue", style="bold red",
                         width=int(self.terminal_width * 0.1))
        table.add_column("Processes", width=int(self.terminal_width * 0.9))
        table.add_row(*self.make_row("New", self.new), end_section=True)
        table.add_row(*self.make_row("Ready", self.ready), end_section=True)
        table.add_row(*self.make_row("Running",
                      self.running, True), end_section=True)
        table.add_row(*self.make_row("Waiting", self.wait), end_section=True)
        table.add_row(*self.make_row("IO", self.io, True), end_section=True)
        table.add_row(*self.make_row("Exit", self.terminate), end_section=True)
        return table

    def out_side_table(self):
        # Creates an outer table with the main queue table and messages side by side.
        table = Table(show_header=False)
        table.add_column("QueeTbale", style="bold cyan")
        message_text = ''.join(self.message)
        table.add_column("Message", width=int(self.terminal_width * 0.3))
        table.add_row(self.generate_table(), message_text, end_section=True)
        return table

    def __rich__(self) -> Panel:
        # Returns a rich Panel for the QueueTable to display in the UI.
        return Panel(self.out_side_table(), title=f"[bold] Queue Steps [/bold]")


class Clock:
    """Renders the time in the center of the screen."""

    def __init__(self, clk, total_process, finished_process, cpu_count, io_count,type):
        # Initializes clock details and system statistics.
        self.clk = clk
        self.total_process = total_process
        self.finished_process = finished_process
        self.cpu_count = cpu_count
        self.io_count = io_count
        self.type=type

    def __rich__(self) -> Panel:
        # Returns a rich Panel showing clock time and system statistics.
        output_str = f"[bold red]Time:[/bold red] [green]{self.clk}[/green]\n"
        output_str += f"[bold red]Algo_Type:[/bold red] [green] {self.type}[/green]   [bold red]CPU_Count:[/bold red] [green] {self.cpu_count}[/green]   [bold red]IO_Count:[/bold red] [green]{self.io_count}[/green]   [bold red]Total_Process:[/bold red] [green]{self.total_process}[/green]  [bold red]Completed_Process:[/bold red] [green]{self.finished_process}[/green]"
        return Panel(Text.from_markup(output_str, justify="center"), title="Clk Time")


# ST = Time entered system
# TAT = Turn Around Time (time exited system - time entered)
# RWT = Time spent in ready queue
# IWT = Time spent in wait queue
class Stats:
    def __init__(self, terminate) -> None:
        # Initializes the statistics table for terminated processes.
        self.table = Table()
        self.console = Console()
        self.terminal_width = self.console.width
        self.terminated = terminate
        self.generate_table()

    def add_row(self):
        # Adds the latest terminated process statistics to the table.
        self.table.rows = []
        if len(self.terminated) > 0:
            current_term = self.terminated[-1]
            pid = current_term.pid
            at = current_term.arrivalTime
            tat = current_term.TurnAroundTime
            rwt = current_term.CPUWaitTime
            iwt = current_term.IOWaitTime
        else:
            pid = ""
            at = ""
            tat = ""
            rwt = ""
            iwt = ""

        self.table.add_row(str(pid), str(at), str(tat), str(rwt), str(iwt))

    def generate_table(self):
        # Creates the table structure for terminated process statistics.
        self.table.add_column("[bold red]Pid[/bold red]",
                              style="bold green", width=int(self.terminal_width * 0.9))
        self.table.add_column("[bold red]Time entered system[/bold red]",
                              style="bold green", width=int(self.terminal_width * 0.9))
        self.table.add_column("[bold red]Turn Around Time[/bold red]",
                              style="bold green", width=int(self.terminal_width * 0.9))
        self.table.add_column("[bold red]Ready Wait Time[/bold red]",
                              style="bold green", width=int(self.terminal_width * 0.9))
        self.table.add_column("[bold red]IO Wait Time[/bold red]",
                              style="bold green", width=int(self.terminal_width * 0.9))
        self.add_row()

        return self.table

    def __rich__(self) -> Panel:
        # Returns a rich Panel for the statistics table.
        return Panel(self.table, title=f"[bold] Job Stats [/bold]")

# A function to create the UI layout combining clock, queue table, and statistics.
def UI_Layout(new, ready, running, wait, IO, exited, clk, messages, total_process, finished_process, cpu_count, io_count,type) -> Layout:
    layout = Layout()
    layout.split(
        Layout(name="header", size=4),
        Layout(name="main"),
    )

    layout["main"].split_column(
        Layout(name="top"),
        Layout(name="bottom"),
    )
    layout['top'].ratio = 2
    layout['bottom'].ratio = 1

    clk_time = Clock(clk, total_process, finished_process, cpu_count, io_count,type)
    table = QueueTable(new, ready, running, wait, IO, exited, messages)
    st = Stats(exited)
    layout['header'].update(clk_time)
    layout['top'].update(table)
    layout['bottom'].update(st)

    return layout

# A class to display overall system statistics like averages and utilizations.
class OverallStat:
    def __init__(self, ATAT, ARWT, AIWT, cpu_util, io_util):
        self.ATAT = ATAT
        self.ARWT = ARWT
        self.AIWT = AIWT
        self.cpu_util = cpu_util
        self.io_util = io_util
        self.console = Console()
        self.terminal_width = self.console.width
        self.table = Table(show_header=True)

    def display_table(self):
        # Displays a table with overall system statistics.
        self.table.add_column("[bold red]Average Turn Around Time[/bold red]",
                              style="bold green", width=int(self.terminal_width * 0.9))
        self.table.add_column("[bold red]Average Ready Wait Time[/bold red]",
                              style="bold green", width=int(self.terminal_width * 0.9))
        self.table.add_column("[bold red]Average IO Wait Time[/bold red]",
                              style="bold green", width=int(self.terminal_width * 0.9))
        self.table.add_column("[bold red]CPU Utilization[/bold red]",
                              style="bold green", width=int(self.terminal_width * 0.9))
        self.table.add_column("[bold red]IO Utilization[/bold red]",
                              style="bold green", width=int(self.terminal_width * 0.9))

        self.table.add_row(str(self.ATAT), str(self.ARWT), str(
            self.AIWT), f"{self.cpu_util:.2f}%", f"{self.io_util:.2f}%")
        panel = Panel(self.table, title=f"[bold]Overall Statistics[/bold] ")
        console = Console()
        console.print(panel)