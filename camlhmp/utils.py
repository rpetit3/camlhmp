import csv
import logging
import sys
from pathlib import Path
from shutil import which
from sys import platform
from typing import Union

import yaml
from Bio import SeqIO
from executor import ExternalCommand, ExternalCommandFailed
from rich import print


def execute(
    cmd,
    directory=Path.cwd(),
    capture=False,
    stdout_file=None,
    stderr_file=None,
    allow_fail=False,
):
    """A simple wrapper around executor."""
    try:
        command = ExternalCommand(
            cmd,
            directory=directory,
            capture=True,
            capture_stderr=True,
            stdout_file=stdout_file,
            stderr_file=stderr_file,
        )

        command.start()
        logging.debug(command.decoded_stdout)
        logging.debug(command.decoded_stderr)

        if capture:
            return [command.decoded_stdout, command.decoded_stderr]
        return True
    except ExternalCommandFailed as e:
        if allow_fail:
            logging.error(e)
            sys.exit(e.returncode)
        else:
            return None


def check_dependencies():
    """
    Check if all dependencies are installed.
    """
    exit_code = 0
    print("Checking dependencies...", file=sys.stderr)
    for program in ["blastn"]:
        which_path = which(program)
        if which_path:
            print(f"Found {program} at {which_path}", file=sys.stderr)
        else:
            print(f"{program} not found", file=sys.stderr)
            exit_code = 1

    if exit_code == 1:
        print("Missing dependencies, please check.", file=sys.stderr)
    else:
        print("You are all set!", file=sys.stderr)
    sys.exit(exit_code)


def get_platform() -> str:
    """
    Get the platform of the executing machine

    Returns:
        str: The platform of the executing machine
    """
    if platform == "darwin":
        return "mac"
    elif platform == "win32":
        # Windows is not supported
        logging.error("Windows is not supported.")
        sys.exit(1)
    return "linux"


def validate_file(filename: str) -> str:
    """
    Validate a file exists and return the absolute path

    Args:
        filename (str): a file to validate exists

    Returns:
        str: absolute path to file
    """
    f = Path(filename)
    if not f.exists():
        raise FileNotFoundError(f"File not found: {filename}")
    return f.absolute()


def file_exists_error(filename: str, force: bool = False):
    """
    Raise a FileExistsError if the file exists and force is False

    Args:
        filename (str): the file to check
        force (bool, optional): force overwrite. Defaults to False.
    """
    if Path(filename).exists() and not force:
        raise FileExistsError(
            f"Results already exists! Use --force to overwrite: {filename}"
        )


def parse_seq(seqfile: str, format: str) -> SeqIO:
    """
    Parse a sequence file.

    Args:
        seqfile (str): input file to be read
        format (str): format of the input file

    Returns:
        SeqIO: the parsed file as a SeqIO object
    """
    with open(seqfile, "rt") as fh:
        return SeqIO.read(fh, format)


def parse_table(
    csvfile: str, delimiter: str = "\t", has_header: bool = True
) -> Union[list, dict]:
    """
    Parse a delimited file.

    Args:
        csvfile (str): input delimited file to be parsed
        delimiter (str, optional): delimter used to separate column values. Defaults to '\t'.
        has_header (bool, optional): the first line should be treated as a header. Defaults to True.

    Returns:
        Union[list, dict]: A dict is returned if a header is present, otherwise a list is returned
    """
    data = []
    with open(csvfile, "rt") as fh:
        for row in (
            csv.DictReader(fh, delimiter=delimiter)
            if has_header
            else csv.reader(fh, delimiter=delimiter)
        ):
            data.append(row)
    return data


def parse_yaml(yamlfile: str) -> Union[list, dict]:
    """
    Parse a YAML file.

    Args:
        yamlfile (str): input YAML file to be read

    Returns:
        Union[list, dict]: the values parsed from the YAML file
    """
    with open(yamlfile, "rt") as fh:
        return yaml.safe_load(fh)


def write_tsv(data: list, output: str):
    """
    Write the dictionary to a TSV file.

    Args:
        data (list): a list of dicts to be written
        output (str): The output file
    """
    logging.debug(f"Writing TSV results to {output}")
    with open(output, "w") as csvfile:
        writer = csv.DictWriter(csvfile, delimiter="\t", fieldnames=data[0].keys())
        writer.writeheader()
        if next(iter(data[0].values())) != "NO_HITS":
            # Data is not empty
            writer.writerows(data)
        else:
            # Data is empty
            logging.debug("NO_HITS found, only writing the column headers")
