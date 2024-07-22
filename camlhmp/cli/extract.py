import logging
import sys
from pathlib import Path

import rich
import rich.console
import rich.traceback
import rich_click as click
from Bio.Seq import Seq
from rich import print
from rich.logging import RichHandler

import camlhmp
from camlhmp.utils import parse_seq, parse_table, validate_file

DB_PATH = str(Path(__file__).parent.absolute()).replace("bin", "data")

# Set up Rich
stderr = rich.console.Console(stderr=True)
rich.traceback.install(console=stderr, width=200, word_wrap=True, extra_lines=1)
click.rich_click.USE_RICH_MARKUP = True
click.rich_click.OPTION_GROUPS = {
    "camlhmp-extract": [
        {
            "name": "Required Options",
            "options": [
                "--path",
                "--targets",
            ],
        },
        {
            "name": "Additional Options",
            "options": [
                "--outdir",
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
    "--path", "-i", required=True, help="The path where input files are located"
)
@click.option(
    "--targets", "-t", required=True, help="A TSV of targets to extract in FASTA format"
)
@click.option(
    "--outdir",
    "-o",
    help="The path to save the extracted targets",
    default="./camlhmp-extract",
)
@click.option("--verbose", is_flag=True, help="Increase the verbosity of output")
@click.option("--silent", is_flag=True, help="Only critical errors will be printed")
def camlhmp(
    path,
    targets,
    outdir,
    verbose,
    silent,
):
    """🐪 camlhmp-extract 🐪 - Extract typing targets from a set of reference sequences"""
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
    reference_path = validate_file(path)
    targets_path = validate_file(targets)

    # Parse the targets TSV
    targets = parse_table(targets_path)
    print(targets)

    # Verify each of the input files exist
    references = {}
    for target in targets:
        if target["file"] not in references:
            references[target["file"]] = {
                "file": validate_file(f"{reference_path}/{target['file']}"),
                "format": target["format"],
            }
            logging.debug(f"Found file: {references[target['file']]['file']}")

    # Parse each of the input files
    seq_objects = {}
    for ref, vals in references.items():
        if vals["format"] in ["fasta", "genbank"]:
            logging.debug(f"Parsing {ref} as {vals['format']}")
            seq_objects[ref] = parse_seq(vals["file"], vals["format"])
        else:
            raise ValueError(f"Unknown format: {vals['format']}")

    # Extract the sequences
    sequences = {}
    for target in targets:
        if target["target"] not in sequences:
            sequences[target["target"]] = []
        logging.debug(
            f"Extracting {target['target']} from {target['file']} ({target['start']}:{target['stop']})"
        )
        sequence = Seq(
            seq_objects[target["file"]].seq[
                int(target["start"]) - 1 : int(target["stop"])
            ]
        )
        if target["strand"] == "-":
            sequence = sequence.reverse_complement()
        sequences[target["target"]].append(
            {
                "accession": target["accession"],
                "type": target["type"],
                "seq": str(sequence),
            }
        )

    # Write the sequences to file (giving each target its own file)
    for target, seqs in sequences.items():
        # create outdir if it doesn't exist
        Path(outdir).mkdir(parents=True, exist_ok=True)
        logging.debug(f"Writing {target} to {outdir}/{target}.fasta")
        with open(f"{outdir}/{target}.fasta", "w") as fh:
            for seq in seqs:
                fh.write(f">{target} {seq['accession']}|{seq['type']}\n{seq['seq']}\n")


def main():
    if len(sys.argv) == 1:
        camlhmp.main(["--help"])
    else:
        camlhmp()


if __name__ == "__main__":
    main()
