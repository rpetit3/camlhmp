import logging
import sys
from pathlib import Path
from shutil import which
from sys import platform
from typing import Union

import yaml
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
