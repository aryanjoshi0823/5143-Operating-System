# rich_table.py

from rich.console import Console
from rich.table import Table

def print_rich_table(headers, data):
    """Prints a formatted table using rich.

    Args:
        headers (list): A list of column headers.
        data (list of lists): A list of rows, where each row is a list of column values.
    """
    # Create a console object for output
    console = Console()

    table = Table(title="ls Command")

    for header in headers:
        table.add_column(header, style="cyan", no_wrap=True)

    for row in data:
        table.add_row(*row)

    console.print(table)
