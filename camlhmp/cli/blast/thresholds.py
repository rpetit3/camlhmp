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
from camlhmp.framework import check_types, get_types, print_camlhmp_version
from camlhmp.parsers.blast import get_blast_target_hits
from camlhmp.utils import file_exists_error, validate_file, parse_seqs, write_tsv

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
                "--blast",
            ],
        },
        {
            "name": "Filtering Options",
            "options": [
                "--min-pident",
                "--min-coverage",
                "--increment",
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
    help="Input file in FASTA format of reference sequences",
)
@click.option(
    "--blast",
    "-b",
    required=False if "--version" in sys.argv else True,
    type=click.Choice(["blastn", "blastp", "blastx", "tblastn", "tblastx"], case_sensitive=True),
    help="The blast algorithm to use",
)
@click.option(
    "--outdir",
    "-o",
    type=click.Path(exists=False),
    default="./camlhmp-blast-thresholds",
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
    default=70,
    show_default=True,
    help="Minimum percent identity to test",
)
@click.option(
    "--min-coverage",
    default=70,
    show_default=True,
    help="Minimum percent coverage to test",
)
@click.option(
    "--increment",
    default=1,
    show_default=True,
    help="The value to increment the thresholds by",
)
@click.option("--force", is_flag=True, help="Overwrite existing reports")
@click.option("--verbose", is_flag=True, help="Increase the verbosity of output")
@click.option("--silent", is_flag=True, help="Only critical errors will be printed")
@click.option("--version", is_flag=True, help="Print schema and camlhmp version")
def camlhmp_blast_thresholds(
    input,
    blast,
    prefix,
    min_pident,
    min_coverage,
    increment,
    outdir,
    force,
    verbose,
    silent,
    version,
):
    """🐪 camlhmp-blast-thresholds 🐪 - Determine the specificity thresholds for a set of reference sequences"""
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

    # If prompted, print the schema and camlhmp version, then exit
    if version:
        print_camlhmp_version()

    # Verify remaining input files
    input_path = validate_file(input)
    logging.debug(f"Processing {input}")

    # Create the output directory
    logging.debug(f"Creating output directory: {outdir}")
    Path(f"{outdir}/reference_seqs").mkdir(parents=True, exist_ok=True)

    # Output files
    thresholds_tsv = f"{outdir}/{prefix}.tsv".replace("//", "/")

    # Make sure output files don't already exist
    file_exists_error(thresholds_tsv, force)

    # Describe the command line arguments
    console = rich.console.Console(stderr=True)
    print(
        "[italic]Running [deep_sky_blue1]camlhmp-blast-thresholds[/deep_sky_blue1] with following parameters:[/italic]",
        file=sys.stderr,
    )
    print(f"[italic]    --input {input}[/italic]", file=sys.stderr)
    print(f"[italic]    --blast {blast}[/italic]", file=sys.stderr)
    print(f"[italic]    --outdir {outdir}[/italic]", file=sys.stderr)
    print(f"[italic]    --prefix {prefix}[/italic]", file=sys.stderr)
    print(f"[italic]    --min-pident {min_pident}[/italic]", file=sys.stderr)
    print(f"[italic]    --min-coverage {min_coverage}[/italic]\n", file=sys.stderr)

    print(
        f"[italic]Gathering seqeuences from {input}...[/italic]",
        file=sys.stderr,
    )

    # Get reference seqeunce names
    reference_seqs = {}
    for seq in parse_seqs(input_path, "fasta"):
        if seq.id not in reference_seqs:
            reference_seqs[seq.id] = []
        reference_seqs[seq.id].append(seq.seq)

    # Write seqs for each reference into separate files
    print(
        f"[italic]Writing reference seqeuences to {outdir}/reference_seqs...[/italic]",
        file=sys.stderr,
    )
    reference_failures = {}
    for ref, seqs in sorted(reference_seqs.items()):
        if ref not in reference_failures:
            reference_failures[ref] = {
                "pident": "-",
                "coverage": "-",
                "hits": "-",
                "comment": "",
            }
        with open(f"{outdir}/reference_seqs/{ref}.fasta", "w") as fh:
            for seq in seqs:
                fh.write(f">{ref}\n{seq}\n")

    # Run blast for each reference seq, adjusting thresholds each time
    references = reference_seqs.keys()
    max_pident_failure = 0
    max_coverage_failure = 0
    for ref in references:
        print(f"Detecting failure for {ref}", file=sys.stderr)
        pident = 100
        has_failure = False
        while pident >= min_pident:
            coverage = 100
            while coverage >= min_coverage:
                # Run blast
                logging.debug(f"Running {ref} with pident={pident} and coverage={coverage}")
                hits, blast_stdout, blast_stderr = run_blast(
                    blast, f"{outdir}/reference_seqs/{ref}.fasta", input_path, pident, coverage
                )
                # Determine if we've gotten a hit that's not the reference, if so, we've failed
                for hit, status in get_blast_target_hits(references, hits).items():
                    if status:
                        if hit.split("_")[0] != ref.split("_")[0]:
                            has_failure = True
                            reference_failures[ref]["pident"] = str(pident)
                            reference_failures[ref]["coverage"] = str(coverage)
                            reference_failures[ref]["hits"] = ",".join(hits)

                            # Determine the max pident and coverage failures
                            if pident > max_pident_failure and pident != 100:
                                max_pident_failure = pident
                            if coverage > max_coverage_failure and coverage != 100:
                                max_coverage_failure = coverage

                            # Add comment about potential overlap or containment
                            if int(coverage) == 100 or int(pident) == 100:
                                reference_failures[ref]["comment"] = "Suspected overlap or containment with another target: "
                            print(
                                f"Detected failure for {ref} with pident={pident} and coverage={coverage} - {hits}",
                                file=sys.stderr,
                            )
                coverage -= increment
                if has_failure:
                    break
            if has_failure:
                break
            pident -= increment

    # Write the results
    print(
        f"[italic]Writing results to {thresholds_tsv}...[/italic]",
        file=sys.stderr,
    )

    # Write the results
    final_results = []
    for ref, vals in sorted(reference_failures.items()):
        final_results.append(
            {
                "reference": ref,
                "pident_failure": vals["pident"],
                "coverage_failure": vals["coverage"],
                "hits": vals["hits"],
                "comment": f"no detection failures for pident>={min_pident} and coverage>={min_coverage}" if vals["hits"] == "-" else vals["comment"],
            }
        )
    write_tsv(final_results, thresholds_tsv)

    # Finalize the results
    print("[italic]Final Results...[/italic]", file=sys.stderr)
    type_table = Table(title=f"Thresholds Detection")
    type_table.add_column("reference", style="white")
    type_table.add_column("pident_failure", style="cyan")
    type_table.add_column("coverage_failure", style="cyan")
    type_table.add_column("hits", style="cyan")
    type_table.add_column("comment", style="cyan")

    for result in final_results:
        type_table.add_row(
            result["reference"],
            result["pident_failure"],
            result["coverage_failure"],
            result["hits"],
            result["comment"],
        )
    console.print(type_table)

    # Print suggested thresholds
    print(
        f"[italic]Suggested thresholds for specificity: pident>{max_pident_failure} and coverage>{max_coverage_failure}[/italic]",
        file=sys.stderr,
    )
    print(
        f"[italic]**NOTE** these are suggestions for a starting point[/italic]",
        file=sys.stderr,
    )


def main():
    if len(sys.argv) == 1:
        camlhmp_blast_thresholds.main(["--help"])
    else:
        camlhmp_blast_thresholds()


if __name__ == "__main__":
    main()
