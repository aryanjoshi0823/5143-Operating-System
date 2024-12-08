import os
import sys
from rich import print
from algorithm.fcfs import FCFS
from algorithm.priorityBased import PriorityBased
from algorithm.roundRobin import RoundRobin


def display_help_message():
    help_message = """[bold green]Usage Examples:[/bold green]
    [cyan]python3 simulation.py type=RR cpus=5 ios=5 timeslice=5 speed=0.01[/cyan]
    [cyan]python3 simulation.py type=FCFS cpus=5 ios=5 speed=0.01[/cyan]
    [cyan]python3 simulation.py type=PB cpus=5 ios=5 speed=0.01[/cyan]
    [cyan]python3 simulation.py type=MLFQ cpus=5 ios=5 speed=0.01[/cyan]

    [bold green]Required Parameters:[/bold green]
        [cyan]type[/cyan]   = algorithm type [FCFS, RR, PB, MLFQ]
        [cyan]cpus[/cyan]   = number of CPU cores (e.g., 5, 2)
        [cyan]ios[/cyan]    = number of IO devices (e.g., 2, 6)

    [bold green]Optional Parameters:[/bold green]
        [cyan]timeslice[/cyan] = required for RR, default 5
        [cyan]speed[/cyan]     = simulation speed, default 0.01
    """
    print(help_message)

def parse_arguments(arguments):
    """Parses command-line arguments."""
    parsed_args = {}
    required_args = ['type', 'cpus', 'ios']

    for arg in arguments:
        if '=' in arg:
            key, value = arg.split('=', 1)
            if not value:
                raise ValueError(f"Missing value for argument: {key}")
            parsed_args[key] = value

    # Check for missing required arguments
    missing_args = [arg for arg in required_args if arg not in parsed_args]
    if missing_args:
        raise ValueError(f"Missing required arguments: {', '.join(missing_args)}")

    # Additional validation for RR
    if parsed_args['type'] == "RR" and "timeslice" not in parsed_args:
        raise ValueError("Missing required argument: timeslice for RR")

    # Convert argument types
    parsed_args['cpus'] = int(parsed_args['cpus'])
    parsed_args['ios'] = int(parsed_args['ios'])
    parsed_args['timeslice'] = int(parsed_args.get('timeslice', 5))
    parsed_args['speed'] = float(parsed_args.get('speed', 0.01))

    return parsed_args

def initialize_scheduler(algorithm_type, cpu_count, io_count, time_slice, speed):

    """Initializes and returns the appropriate scheduler based on the algorithm type."""

    if algorithm_type == "FCFS":
        return FCFS(cpu_count, io_count, time_slice, algorithm_type, speed)
    
    elif algorithm_type == "PB":
        return PriorityBased(cpu_count, io_count, time_slice, algorithm_type, speed)

    elif algorithm_type == "RR":
        return RoundRobin(cpu_count, io_count, time_slice, algorithm_type, speed)

    elif algorithm_type == "MLFQ":
        print("[bold yellow]Initializing MLFQ Scheduler[/bold yellow]")

    else:
        raise ValueError("Algorithm type should be one of: FCFS, RR, PB, MLFQ")


if __name__ == '__main__':
    try:
        if len(sys.argv) < 2:
            raise ValueError("No arguments provided")

        # Parse arguments
        parsed_args = parse_arguments(sys.argv[1:])
        
        # Initialize the appropriate scheduler
        scheduler = initialize_scheduler(
            parsed_args['type'],
            parsed_args['cpus'],
            parsed_args['ios'],
            parsed_args['timeslice'],
            parsed_args['speed']
        )

        # Run the scheduler if it's valid
        if scheduler:
            print(f"[bold green]Running {parsed_args['type']} Scheduler...[/bold green]")
            scheduler.run_algorithm()
        else:
            print("[bold red]No valid scheduler found to run![/bold red]")

    except ValueError as e:
        print(f"[bold red]Error:[/bold red] {e}\n")
        display_help_message()
        sys.exit(1)











