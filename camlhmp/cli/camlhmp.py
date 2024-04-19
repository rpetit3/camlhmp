import json
import logging
import sys
from pathlib import Path

import rich
import rich.console
import rich.traceback
import rich_click as click
from rich import print
from rich.logging import RichHandler
from rich.table import Table

import camlhmp
from camlhmp.engines.blast import run_blastn, get_blast_target_hits
from camlhmp.framework import read_framework, get_profiles, check_profiles
from camlhmp.visuals.framework import describe_framework
from camlhmp.utils import validate_file

DB_PATH = str(Path(__file__).parent.absolute()).replace("bin", "data")

# Set up Rich
stderr = rich.console.Console(stderr=True)
rich.traceback.install(console=stderr, width=200, word_wrap=True, extra_lines=1)
click.rich_click.USE_RICH_MARKUP = True
click.rich_click.OPTION_GROUPS = {
    "camlhmp": [
        {
            "name": "Required Options",
            "options": [
                "--input",
                "--yaml",
                "--targets",
            ]
        },
        {
            "name": "Filtering Options",
            "options": [
                "--min-pident",
                "--min-coverage",
            ],
        },
        {
            "name": "Additional Options",
            "options": [
                "--verbose",
                "--silent",
                "--version",
                "--help",
            ],
        },
    ]
}


@click.command()
@click.version_option(camlhmp.__version__, "--version", "-V")
@click.option("--input", "-i", required=True, help="Input file in FASTA format to classify")
@click.option("--yaml", "-y", required=True, help="YAML file documenting the targets and profiles")
@click.option("--targets", "-t", required=True, help="Query targets in FASTA format")
@click.option(
    "--min-pident",
    default=95,
    show_default=True,
    help="Minimum percent identity to count a hit",
)
@click.option(
    "--min-coverage",
    default=95,
    show_default=True,
    help="Minimum percent coverage to count a hit",
)
@click.option("--verbose", is_flag=True, help="Increase the verbosity of output")
@click.option("--silent", is_flag=True, help="Only critical errors will be printed")
def camlhmp(
    input,
    yaml,
    targets,
    min_pident,
    min_coverage,
    verbose,
    silent,
):
    """🐪 camlhmp ([i]camel hump[/i])🐪 - [u]C[/u]lassification through y[u]AML[/u] [u]H[/u]euristic [u]M[/u]apping [u]P[/u]rotocol"""
    # Setup logs
    logging.basicConfig(
        format="%(asctime)s:%(name)s:%(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            RichHandler(rich_tracebacks=True, console=rich.console.Console(stderr=True))
        ],
    )
    logging.getLogger().setLevel(
        logging.ERROR if silent else logging.DEBUG if verbose else logging.INFO
    )

    abspath = validate_file(input)
    logging.debug(f"Processing {abspath}")

    # Verify input files are available
    input_path = validate_file(input)
    yaml_path = validate_file(yaml)
    targets_path = validate_file(targets)

    # Read the YAML file
    framework = read_framework(yaml_path)
    #describe_framework(framework)

    console = rich.console.Console(stderr=True)
    print("[italic]Running [deep_sky_blue1]camlhmp[/deep_sky_blue1] with following parameters:[/italic]", file=sys.stderr)
    print(f"[italic]    --input {input}[/italic]", file=sys.stderr)
    print(f"[italic]    --yaml {yaml}[/italic]", file=sys.stderr)
    print(f"[italic]    --targets {targets}[/italic]", file=sys.stderr)
    print(f"[italic]    --min_pident {min_pident}[/italic]", file=sys.stderr)
    print(f"[italic]    --min_coverage {min_coverage}[/italic]\n", file=sys.stderr)

    profile_hits = None
    if framework['engine']['tool'] == "blastn":
        # Run BLASTN
        print("[italic]Running BLASTN...[/italic]", file=sys.stderr)
        blast_stdout, blast_stderr = run_blastn(input_path, targets_path, min_pident, min_coverage)
        target_results = get_blast_target_hits(framework['targets'], blast_stdout)

        print("[italic]Processing hits...[/italic]", file=sys.stderr)
        profiles = get_profiles(framework)
        profile_hits = check_profiles(profiles, target_results)

    if profile_hits:
        print("[italic]Final Results...[/italic]", file=sys.stderr)
        profile_table = Table(title=f"{framework['metadata']['name']}")
        profile_table.add_column("profile", style="white")
        profile_table.add_column("status", style="cyan")

        for profile, status in profile_hits.items():
            profile_table.add_row(profile, str(status))
        console.print(profile_table)

def main():
    if len(sys.argv) == 1:
        camlhmp.main(["--help"])
    else:
        camlhmp()


if __name__ == "__main__":
    main()
