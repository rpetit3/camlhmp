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
from camlhmp.engines.blast import get_blast_target_hits, run_blastn
from camlhmp.framework import check_types, get_types, read_framework
from camlhmp.utils import file_exists_error, validate_file, write_tsv
from camlhmp.visuals.framework import describe_framework

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
@click.version_option(camlhmp.__version__, "--version", "-V")
@click.option(
    "--input", "-i", required=True, help="Input file in FASTA format to classify"
)
@click.option(
    "--yaml",
    "-y",
    required=True,
    default=os.environ.get("CAML_YAML", ""),
    show_default=True,
    help="YAML file documenting the targets and types",
)
@click.option(
    "--targets",
    "-t",
    required=True,
    default=os.environ.get("CAML_TARGETS", ""),
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
def camlhmp(
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
):
    """🐪 camlhmp-blast 🐪 - Classify assemblies with a camlhmp schema using BLAST"""
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

    # Create the output directory
    logging.debug(f"Creating output directory: {outdir}")
    Path(outdir).mkdir(parents=True, exist_ok=True)

    # Verify input files are available
    input_path = validate_file(input)
    yaml_path = validate_file(yaml)
    targets_path = validate_file(targets)
    logging.debug(f"Processing {targets}")

    # Read the YAML file
    framework = read_framework(yaml_path)

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
    if framework["engine"]["tool"] not in ["blastn"]:
        raise ValueError(
            f"Unsupported engine ({framework['engine']['tool']}), camlhmp-blast only supports blast"
        )

    # Run blast
    print(f"[italic]Running {framework['engine']['tool']}...[/italic]", file=sys.stderr)
    hits, blast_stdout, blast_stderr = run_blastn(
        input_path, targets_path, min_pident, min_coverage
    )
    target_results = get_blast_target_hits(framework["targets"], hits)

    # Rrocess the hits against the types
    print("[italic]Processing hits...[/italic]", file=sys.stderr)
    types = get_types(framework)
    type_hits = check_types(types, target_results)

    # Finalize the results
    print("[italic]Final Results...[/italic]", file=sys.stderr)
    type_table = Table(title=f"{framework['metadata']['name']}")
    type_table.add_column("sample", style="white")
    type_table.add_column("type", style="white")
    type_table.add_column("targets", style="cyan")
    type_table.add_column("schema", style="cyan")
    type_table.add_column("version", style="cyan")
    type_table.add_column("comment", style="cyan")

    final_type = []
    final_targets = []

    # Get a list of targets that met the threshold
    for target, status in target_results.items():
        if status:
            final_targets.append(target)

    # Get the final type(s)
    final_details = []
    for type, vals in type_hits.items():
        final_details.append(
            {
                "sample": prefix,
                "type": type,
                "status": vals["status"],
                "targets": ",".join(vals["targets"]),
                "missing": ",".join(vals["missing"]),
                "schema": framework["metadata"]["id"],
                "version": framework["metadata"]["version"],
                "comment": vals["comment"],
            }
        )
        if vals["status"]:
            final_type.append(type)

    # Generate a comment based on the results
    comment = ""
    if not len(final_type):
        if len(final_targets):
            comment = "A type could not be determined, but one or more targets found"
        else:
            comment = "A type could not be determined"
    elif len(final_type) > 1:
        comment = f"Found matches for multiple types including: {', '.join(final_type)}"
        final_type = ["multiple"]

    final_type = ",".join(final_type) if len(final_type) > 0 else "-"
    type_table.add_row(
        prefix,
        final_type,
        ",".join(final_targets),
        framework["metadata"]["id"],
        framework["metadata"]["version"],
        comment,
    )
    console.print(type_table)

    # Write the results
    print("[italic]Writing outputs...[/italic]", file=sys.stderr)

    # Write final prediction
    final_result = {
        "sample": prefix,
        "type": final_type,
        "targets": ",".join(final_targets),
        "schema": framework["metadata"]["id"],
        "version": framework["metadata"]["version"],
        "comment": comment,
    }
    print(
        f"[italic]Final predicted type written to [deep_sky_blue1]{result_tsv}[/deep_sky_blue1][/italic]",
        file=sys.stderr,
    )
    write_tsv([final_result], result_tsv)

    # Write details for each type
    print(
        f"[italic]Results against each type written to [deep_sky_blue1]{details_tsv}[/deep_sky_blue1][/italic]",
        file=sys.stderr,
    )
    write_tsv(final_details, details_tsv)

    # Write blast results
    print(
        f"[italic]{framework['engine']['tool']} results written to [deep_sky_blue1]{blast_tsv}[/deep_sky_blue1][/italic]",
        file=sys.stderr,
    )
    write_tsv(blast_stdout, blast_tsv)


def main():
    if len(sys.argv) == 1:
        camlhmp.main(["--help"])
    else:
        camlhmp()


if __name__ == "__main__":
    main()
