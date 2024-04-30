"""
A set of functions for working with the caml framework.
"""

import logging

from rich import print
from rich.panel import Panel
from rich.text import Text

from camlhmp.utils import parse_yaml


def read_framework(yamlfile: str) -> dict:
    """
    Read the framework YAML file.

    Args:
        yamlfile (str): input YAML file to be read

    Returns:
        dict: the parsed YAML file
    """
    return parse_yaml(yamlfile)


def get_types(framework: dict) -> dict:
    """
    Get the types from the framework.

    Example framework:
    aliases:
    - name: "ccr Type 2"
      targets: ["ccrA1", "ccrB1"]
    types:
    - name: "I"
      targets:
        - "ccr Type 1"
        - "mec Class B"

    Args:
        framework (dict): the parsed YAML framework

    Returns:
        dict: the types with associated targets
    """
    types = {}
    aliases = {}

    # If aliases are present, save their targets
    if "aliases" in framework:
        for alias in framework["aliases"]:
            aliases[alias["name"]] = alias["targets"]

    # Save the types and their targets
    for profile in framework["types"]:
        types[profile["name"]] = {
            "targets": [],
            "excludes": [],
        }
        for target in profile["targets"]:
            if target in aliases:
                types[profile["name"]]["targets"] = [
                    *types[profile["name"]]["targets"],
                    *aliases[target],
                ]
            elif target in framework["targets"]:
                types[profile["name"]]["targets"].append(target)
            else:
                raise ValueError(f"Target {target} not found in framework")

        # Capture any targets that should cause a profile to fail
        if "excludes" in profile:
            for exclude in profile["excludes"]:
                if exclude in aliases:
                    types[profile["name"]]["excludes"] = [
                        *types[profile["name"]]["excludes"],
                        *aliases[exclude],
                    ]
                elif exclude in framework["targets"]:
                    types[profile["name"]]["excludes"].append(exclude)
                else:
                    raise ValueError(f"Target {exclude} not found in framework")

    # Debugging information
    logging.debug("camlhmp.framework.get_types")
    logging.debug(f"Aliases: {framework['aliases']}")
    logging.debug(f"Targets: {framework['targets']}")
    logging.debug(f"Types: {types}")

    return types


def check_types(types: dict, results: dict) -> dict:
    """
    Check the types against the results.

    Args:
        types (dict): the types with associated targets
        results (dict): the BLAST results

    Returns:
        dict: the types and their outcome
    """
    type_hits = {}
    for type, vals in types.items():
        targets = vals["targets"]
        excludes = vals["excludes"]
        type_hits[type] = {
            "status": False,
            "targets": [],
            "missing": [],
            "comment": "",
        }
        matched_all_targets = True
        for target in targets:
            if results[target]:
                type_hits[type]["targets"].append(target)
            else:
                type_hits[type]["missing"].append(target)
                matched_all_targets = False

        # Check if any of the excludes are present
        for exclude in excludes:
            if results[exclude]:
                type_hits[type][
                    "comment"
                ] = f"Excluded target {exclude} found, failing type {type}"
                logging.debug(f"Excluded target {exclude} found, failing type {type}")
                matched_all_targets = False
        type_hits[type]["status"] = matched_all_targets

    # Debugging information
    logging.debug("camlhmp.framework.check_types")
    logging.debug(f"Type Hits: {type_hits}")

    return type_hits
