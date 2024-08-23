"""
A set of functions for working with the caml framework.
"""
import sys
import logging

from rich import print

import camlhmp
from camlhmp.utils import parse_yaml


def read_framework(yamlfile: str) -> dict:
    """
    Read the framework YAML file.

    Args:
        yamlfile (str): input YAML file to be read

    Returns:
        dict: the parsed YAML file

    Examples:
        >>> from camlhmp.framework import read_framework
        >>> framework = read_framework(yaml_path)
    """
    return parse_yaml(yamlfile)


def print_camlhmp_version() -> None:
    """
    Print the version of camlhmp, then exit

    Args:
        framework (dict): the parsed YAML framework

    Examples:
        >>> from camlhmp.framework import print_camlhmp_version
        >>> print_camlhmp_version()
    """
    print(f"camlhmp, version {camlhmp.__version__}", file=sys.stderr)
    sys.exit(0)


def print_version(framework: dict) -> None:
    """
    Print the version of the framework, then exit

    Args:
        framework (dict): the parsed YAML framework

    Examples:
        >>> from camlhmp.framework import print_version
        >>> print_version(framework)
    """
    print(f"camlhmp, version {camlhmp.__version__}", file=sys.stderr)
    print(f"schema {framework['metadata']['id']}, version {framework['metadata']['version']}", file=sys.stderr)
    sys.exit(0)


def print_versions(frameworks: list) -> None:
    """
    Print the version of the framework, then exit

    Args:
        frameworks (list[dict]): A list of parsed YAML frameworks

    Examples:
        >>> from camlhmp.framework import print_version
        >>> print_versions([framework1, framework2])
    """
    print(f"camlhmp, version {camlhmp.__version__}", file=sys.stderr)
    for framework in frameworks:
        print(f"schema {framework['metadata']['id']}, version {framework['metadata']['version']}", file=sys.stderr)
    sys.exit(0)


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

    Examples:
        >>> from camlhmp.framework import get_types
        >>> types = get_types(framework)
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
    if "aliases" in framework:
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

    Examples:
        >>> from camlhmp.framework import check_types
        >>> type_hits = check_types(types, target_results)
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


def check_regions(types: dict, results: dict, min_coverage: int) -> dict:
    """
    Check the region types against the results.

    Args:
        types (dict): the types with associated targets
        results (dict): the BLAST results
        min_coverage (int): the minimum coverage required for a region

    Returns:
        dict: the types and their outcome

    Examples:
        >>> from camlhmp.framework import check_regions
        >>> type_hits = check_regions(types, target_results, min_coverage)
    """
    type_hits = {}
    for type, vals in types.items():
        targets = vals["targets"]
        excludes = vals["excludes"]
        type_hits[type] = {
            "status": False,
            "targets": [],
            "missing": [],
            "coverage": [],
            "hits": [],
            "comment": [],
        }
        matched_all_targets = True
        for target in targets:
            if target in results:
                if results[target]["coverage"] >= min_coverage:
                    type_hits[type]["targets"].append(target)
                else:
                    type_hits[type]["missing"].append(target)
                    matched_all_targets = False

                type_hits[type]["coverage"].append(f"{results[target]['coverage']:.2f}")
                type_hits[type]["hits"].append(str(len(results[target]["hits"])))
                if len(targets) > 1:
                    if results[target]["comment"]:
                        formatted_comments = []
                        for comment in results[target]["comment"]:
                            formatted_comments.append(f"{target}:{comment}")
                        if formatted_comments:
                            type_hits[type]["comment"].append(
                                ";".join(formatted_comments)
                            )
                else:
                    if results[target]["comment"]:
                        type_hits[type]["comment"].append(
                            ";".join(results[target]["comment"])
                        )
            else:
                matched_all_targets = False

        # Check if any of the excludes are present
        for exclude in excludes:
            if results[exclude]:
                if results[exclude]["coverage"] >= min_coverage:
                    type_hits[type]["comment"].append(
                        f"Excluded target {exclude} found, failing type {type}"
                    )
                    logging.debug(
                        f"Excluded target {exclude} found, failing type {type}"
                    )
                    matched_all_targets = False

        type_hits[type]["status"] = matched_all_targets

    # Debugging information
    logging.debug("camlhmp.framework.check_regions")
    logging.debug(f"Type Hits: {type_hits}")

    return type_hits
