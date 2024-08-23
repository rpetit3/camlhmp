import csv
import logging
import string
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
    """
    A simple wrapper around executor.
    
    Args:
        cmd (str): The command to be executed
        directory (Path, optional): The directory to execute the command in. Defaults to Path.cwd().
        capture (bool, optional): Capture the output of the command. Defaults to False.
        stdout_file (Path, optional): The file to write stdout to. Defaults to None.
        stderr_file (Path, optional): The file to write stderr to. Defaults to None.
        allow_fail (bool, optional): Allow the command to fail. Defaults to False.

    Returns:
        Union[bool, list]: True if successful, otherwise a list of stdout and stderr

    Raises:
        ExternalCommandFailed: If the command fails and allow_fail is True

    Examples:
        >>> from camlhmp.utils import execute
        >>> stdout, stderr = execute(
                f"{cat_type} {subject} | {engine} -query {query} -subject - -outfmt '6 {outfmt}' {qcov_hsp_perc} {perc_identity}",
                capture=True,
            )
    """
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

    Examples:
        >>> from camlhmp.utils import check_dependencies
        >>> check_dependencies()
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

    Examples:
        >>> from camlhmp.utils import get_platform
        >>> platform = get_platform()
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
    Validate a file exists and not empty, if passing return the absolute path

    Args:
        filename (str): a file to validate exists

    Returns:
        str: absolute path to file

    Raises:
        FileNotFoundError: if the file does not exist
        ValueError: if the file is empty

    Examples:
        >>> from camlhmp.utils import validate_file
        >>> file = validate_file("data.fasta")
    """
    f = Path(filename)
    if not f.exists():
        raise FileNotFoundError(f"File ('{filename}') not found, cannot continue")
    elif f.stat().st_size == 0:
        raise ValueError(f"File ('{filename}') is empty, cannot continue")
    return f.absolute()


def validate_engine(tool: str, engine: str, accepted: list) -> str:
    """
    Validate the engine is in the accepted list.

    Args:
        tool (str): the tool to validate
        engine (str): the engine to validate
        accepted (list): a list of accepted engines

    Raises:
        ValueError: if the engine is not in the accepted list

    Examples:
        >>> from camlhmp.utils import validate_engine
        >>> validate_engine("blast", ["blast"])
    """
    if engine not in accepted:
        raise ValueError(f"Unsupported engine ('{engine}'), {tool} only supports: {accepted}")
    return engine


def file_exists_error(filename: str, force: bool = False):
    """
    Determine if a file exists and raise an error if it does.

    Args:
        filename (str): the file to check
        force (bool, optional): force overwrite. Defaults to False.

    Raises:
        FileExistsError: if the file exists and force is False
    """
    if Path(filename).exists() and not force:
        raise FileExistsError(
            f"Results already exists! Use --force to overwrite: {filename}"
        )


def parse_seq(seqfile: str, format: str) -> SeqIO:
    """
    Parse a sequence file containing a single record.

    Args:
        seqfile (str): input file to be read
        format (str): format of the input file

    Returns:
        SeqIO: the parsed file as a SeqIO object

    Examples:
        >>> from camlhmp.utils import parse_seq
        >>> seq = parse_seq("data.fasta", "fasta")
    """
    with open(seqfile, "rt") as fh:
        return SeqIO.read(fh, format)


def parse_seqs(seqfile: str, format: str) -> SeqIO:
    """
    Parse a sequence file containing a multiple records.

    Args:
        seqfile (str): input file to be read
        format (str): format of the input file

    Returns:
        SeqIO: the parsed file as a SeqIO object

    Examples:
        >>> from camlhmp.utils import parse_seqs
        >>> seqs = parse_seqs("data.fasta", "fasta")
    """
    with open(seqfile, "rt") as fh:
        return list(SeqIO.parse(fh, format))


def parse_seq_lengths(seqfile: str, format: str) -> dict:
    """
    Parse a sequence file and return the lengths of the sequences.

    Args:
        seqfile (str): input file to be read
        format (str): format of the input file

    Returns:
        dict: a dictionary of sequence lengths

    Examples:
        >>> from camlhmp.utils import parse_seq_lengths
        >>> lengths = parse_seq_lengths("data.fasta", "fasta")
    """
    lengths = {}
    for seq in parse_seqs(seqfile, "fasta"):
        logging.debug(f"Processing {seq.id} with length {len(seq.seq)}")
        lengths[seq.id] = len(seq.seq)
    return lengths


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

    Examples:
        >>> from camlhmp.utils import parse_table
        >>> data = parse_table("data.tsv")
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

    Examples:
        >>> from camlhmp.utils import parse_yaml
        >>> data = parse_yaml("data.yaml")
    """
    with open(yamlfile, "rt") as fh:
        return yaml.safe_load(fh)


def write_tsv(data: list, output: str):
    """
    Write the dictionary to a TSV file.

    Args:
        data (list): a list of dicts to be written
        output (str): The output file

    Examples:
        >>> from camlhmp.utils import write_tsv
        >>> write_tsv(data, "results.tsv")
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


def remove_lowercase(s: str) -> str:
    """
    Remove lowercase characters from a string.

    Args:
        s (str): input string to be processed

    Returns:
        str: the string with lowercase characters removed

    Examples:
        >>> from camlhmp.utils import remove_lowercase
        >>> s = remove_lowercase("ABCdef")
    """
    table = str.maketrans('', '', string.ascii_lowercase)
    return s.translate(table)
