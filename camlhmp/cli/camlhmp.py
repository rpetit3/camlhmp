import sys

import rich
import rich.console
import rich.traceback
import rich_click as click
from rich import print
from rich.logging import RichHandler
from rich.table import Table

import camlhmp

# List of available commands
COMMANDS = {
    "camlhmp-blast": "Classify assemblies with a camlhmp schema using BLAST",
    "camlhmp-extract": "Extract typing targets from a set of reference sequences",
}

# Set up Rich
stderr = rich.console.Console(stderr=True)
rich.traceback.install(console=stderr, width=200, word_wrap=True, extra_lines=1)
click.rich_click.USE_RICH_MARKUP = True
click.rich_click.OPTION_GROUPS = {
    "camlhmp": [
        {
            "name": "Additional Options",
            "options": [
                "--version",
                "--help",
            ],
        },
    ]
}


@click.command()
@click.version_option(camlhmp.__version__, "--version", "-V")
def camlhmp():
    """🐪 camlhmp ([i]camel hump[/i])🐪 - [u]C[/u]lassification through y[u]AML[/u] [u]H[/u]euristic [u]M[/u]apping [u]P[/u]rotocol"""

    console = rich.console.Console(stderr=True)
    print(
        "[bold]🐪 camlhmp 🐪[/bold] - Classification through YAML Heuristic Mapping Protocol\n"
    )
    type_table = Table(title="Available camlhmp commands")
    type_table.add_column("command", style="white")
    type_table.add_column("description", style="white")

    for command, description in COMMANDS.items():
        type_table.add_row(command, description)
    console.print(type_table)


def main():
    camlhmp()


if __name__ == "__main__":
    main()
