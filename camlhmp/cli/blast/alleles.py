import logging
import os
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
from camlhmp.engines.blast import run_blast
from camlhmp.framework import check_types, get_types, print_version, read_framework
from camlhmp.parsers.blast import get_blast_allele_hits
from camlhmp.utils import file_exists_error, validate_file, write_tsv

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
            ],
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
                "--prefix",
                "--outdir",
                "--force",
                "--verbose",
                "--silent",
                "--version",
                "--help",
            ],
        },
    ]
}


@click.command()
@click.option(
    "--input",
    "-i",
    required=False if "--version" in sys.argv else True,
    help="Input file in FASTA format to classify",
)
@click.option(
    "--yaml",
    "-y",
    required=True,
    default=os.environ.get("CAML_YAML", None),
    show_default=True,
    help="YAML file documenting the targets and types",
)
@click.option(
    "--targets",
    "-t",
    required=False if "--version" in sys.argv else True,
    default=os.environ.get("CAML_TARGETS", None),
    show_default=True,
    help="Query targets in FASTA format",
)
@click.option(
    "--outdir",
    "-o",
    type=click.Path(exists=False),
    default="./",
    show_default=True,
    help="Directory to write output",
)
@click.option(
    "--prefix",
    "-p",
    type=str,
    default="camlhmp",
    show_default=True,
    help="Prefix to use for output files",
)
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
@click.option("--force", is_flag=True, help="Overwrite existing reports")
@click.option("--verbose", is_flag=True, help="Increase the verbosity of output")
@click.option("--silent", is_flag=True, help="Only critical errors will be printed")
@click.option("--version", is_flag=True, help="Print schema and camlhmp version")
def camlhmp_blast_alleles(
    input,
    yaml,
    targets,
    prefix,
    outdir,
    min_pident,
    min_coverage,
    force,
    verbose,
    silent,
    version,
):
    """🐪 camlhmp-blast-alleles 🐪 - Classify assemblies using BLAST against alleles of a set of genes"""
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

    # Verify input files are available
    yaml_path = validate_file(yaml)

    # Read the YAML file
    framework = read_framework(yaml_path)

    # If prompted, print the schema and camlhmp version, then exit
    if version:
        print_version(framework)

    # Verify remaining input files
    input_path = validate_file(input)
    targets_path = validate_file(targets)
    logging.debug(f"Processing {targets}")

    # Create the output directory
    logging.debug(f"Creating output directory: {outdir}")
    Path(outdir).mkdir(parents=True, exist_ok=True)

    # Output files
    result_tsv = f"{outdir}/{prefix}.tsv".replace("//", "/")
    blast_tsv = f"{outdir}/{prefix}.{framework['engine']['tool']}.tsv".replace(
        "//", "/"
    )
    details_tsv = f"{outdir}/{prefix}.details.tsv".replace("//", "/")

    # Make sure output files don't already exist
    file_exists_error(result_tsv, force)
    file_exists_error(blast_tsv, force)
    file_exists_error(details_tsv, force)

    # Describe the command line arguments
    console = rich.console.Console(stderr=True)
    print(
        "[italic]Running [deep_sky_blue1]camlhmp[/deep_sky_blue1] with following parameters:[/italic]",
        file=sys.stderr,
    )
    print(f"[italic]    --input {input}[/italic]", file=sys.stderr)
    print(f"[italic]    --yaml {yaml}[/italic]", file=sys.stderr)
    print(f"[italic]    --targets {targets}[/italic]", file=sys.stderr)
    print(f"[italic]    --outdir {outdir}[/italic]", file=sys.stderr)
    print(f"[italic]    --prefix {prefix}[/italic]", file=sys.stderr)
    print(f"[italic]    --min-pident {min_pident}[/italic]", file=sys.stderr)
    print(f"[italic]    --min-coverage {min_coverage}[/italic]\n", file=sys.stderr)

    print(
        f"[italic]Starting camlhmp for {framework['metadata']['name']}...[/italic]",
        file=sys.stderr,
    )

    # Verify the engine is a support blast subcommand
    if framework["engine"]["type"] not in ["blast"]:
        raise ValueError(
            f"Unsupported engine ({framework['engine']['type']}), camlhmp-blast-alleles only supports blast"
        )

    # Run blast
    print(f"[italic]Running {framework['engine']['tool']}...[/italic]", file=sys.stderr)
    hits, blast_stdout, blast_stderr = run_blast(
        framework["engine"]["tool"], input_path, targets_path, min_pident, min_coverage
    )

    # Process the hits against the types
    print("[italic]Processing hits...[/italic]", file=sys.stderr)
    target_results = get_blast_allele_hits(framework["targets"], blast_stdout, min_pident, min_coverage)

    # Finalize the results
    print("[italic]Final Results...[/italic]", file=sys.stderr)
    type_table = Table(title=f"{framework['metadata']['name']}")
    type_table.add_column("sample", style="white")
    type_table.add_column("schema", style="cyan")
    type_table.add_column("schema_version", style="cyan")
    type_table.add_column("camlhmp_version", style="cyan")
    type_table.add_column("params", style="cyan")
    for target in target_results:
        type_table.add_column(f"{target}_id", style="cyan")
        type_table.add_column(f"{target}_pident", style="cyan")
        type_table.add_column(f"{target}_qcovs", style="cyan")
        type_table.add_column(f"{target}_bitscore", style="cyan")
        type_table.add_column(f"{target}_comment", style="cyan")

    # Get the final type(s)
    final_details = []
    final_row = {
        "sample": prefix,
        "schema": framework["metadata"]["id"],
        "schema_version": framework["metadata"]["version"],
        "camlhmp_version": camlhmp.__version__,
        "params": f"min-coverage={min_coverage};min-pident={min_pident}",
    }
    for target in target_results:
        final_row[f"{target}_id"] = target_results[target]["id"]
        final_row[f"{target}_pident"] = str(target_results[target]["pident"])
        final_row[f"{target}_qcovs"] = str(target_results[target]["qcovs"])
        final_row[f"{target}_bitscore"] = str(target_results[target]["bitscore"])
        final_row[f"{target}_comment"] = target_results[target]["comment"]

    # Generate a comment based on the results
    type_table.add_row(
        *final_row.values(),
    )
    console.print(type_table)

    # Write the results
    print("[italic]Writing outputs...[/italic]", file=sys.stderr)

    # Write final prediction
    print(
        f"[italic]Final predicted type written to [deep_sky_blue1]{result_tsv}[/deep_sky_blue1][/italic]",
        file=sys.stderr,
    )
    write_tsv([final_row], result_tsv)

    # Write blast results
    print(
        f"[italic]{framework['engine']['tool']} results written to [deep_sky_blue1]{blast_tsv}[/deep_sky_blue1][/italic]",
        file=sys.stderr,
    )
    write_tsv(blast_stdout, blast_tsv)


def main():
    if len(sys.argv) == 1:
        camlhmp_blast_alleles.main(["--help"])
    else:
        camlhmp_blast_alleles()


if __name__ == "__main__":
    main()
