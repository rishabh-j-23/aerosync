from typing import Sequence

import click
from tabulate import tabulate


def print_sequences(entries: Sequence, headers=None):
    if not entries:
        click.echo("No records found")
        return

    # If no headers provided, use the keys of the first entry
    if not headers:
        headers = list(entries[0].model_dump().keys())

    # Create rows by matching the header order for each entry's values
    rows = [[entry.model_dump().get(header) for header in headers] for entry in entries]

    click.echo(tabulate(rows, headers=headers, tablefmt="grid"))
