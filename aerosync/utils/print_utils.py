import logging
from typing import List, Sequence

import click
from pydantic import BaseModel
from tabulate import tabulate


def print_table(entries: list):
    logging.info(f"entries={entries}")
    if not entries:
        click.echo("No records found.")
        return

    # If entries are Pydantic models or ORM objects, convert to dict
    if isinstance(entries[0], BaseModel):
        data = [entry.dict() for entry in entries]
    else:
        data = [entry.__dict__ for entry in entries]

    # Extract headers from keys
    headers = data[0].keys()

    # Extract rows
    rows = [list(item.values()) for item in data]

    # Print table
    click.echo(tabulate(rows, headers=headers, tablefmt="grid"))


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
