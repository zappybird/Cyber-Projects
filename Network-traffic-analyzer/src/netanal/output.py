from rich.table import Table
from rich.console import Console

console = Console()

def print_protocol_table(stats):
    table = Table(title="Protocol Distribution")
    table.add_column("Protocol")
    table.add_column("Count")

    for proto, count in stats.protocol_counts.items():
        table.add_row(proto, str(count))

    console.print(table)
