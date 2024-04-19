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


def get_profiles(framework: dict) -> dict:
    """
    Get the profiles from the framework.

    Example framework:
    aliases:
    - name: "ccr Type 2"
      targets: ["ccrA1", "ccrB1"]
    profiles:
    - name: "I"
      targets:
        - "ccr Type 1"
        - "mec Class B"

    Args:
        framework (dict): the parsed YAML framework

    Returns:
        dict: the profiles with associated targets
    """
    profiles = {}
    aliases = {}

    # If aliases are present, save their targets
    if "aliases" in framework:
        for alias in framework["aliases"]:
            aliases[alias["name"]] = alias["targets"]

    # Save the profiles and their targets
    for profile in framework["profiles"]:
        profiles[profile["name"]] = []
        for target in profile['targets']:
            if target in aliases:
                profiles[profile["name"]] = [*profiles[profile["name"]], *aliases[target]]
            elif target in framework['targets']:
                profiles[profile["name"]].append(target)
            else:
                raise ValueError(f"Target {target} not found in framework")

    # Debugging information
    logging.debug("camlhmp.framework.get_profiles")
    logging.debug(f"Aliases: {framework["aliases"]}")
    logging.debug(f"Targets: {framework["targets"]}")
    logging.debug(f"Profiles: {profiles}")

    return profiles


def check_profiles(profiles: dict, results: dict) -> dict:
    """
    Check the profiles against the results.

    Args:
        profiles (dict): the profiles with associated targets
        results (dict): the BLAST results

    Returns:
        dict: the profiles and their outcome
    """
    profile_hits = {}
    for profile, targets in profiles.items():
        profile_hits[profile] = {}
        matched_all_targets = True
        for target in targets:
            if not results[target]:
                matched_all_targets = False
        profile_hits[profile] = matched_all_targets

    # Debugging information
    logging.debug("camlhmp.framework.check_profiles")
    logging.debug(f"Profile Hits: {profile_hits}")

    return profile_hits
