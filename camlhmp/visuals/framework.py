"""
A set of functions to assist with printing the framework YAML file.
"""

from rich import print
from rich.panel import Panel
from rich.text import Text


def describe_framework(framework: str) -> None:
    """
    Print the framework YAML file.

    Args:
        yamlfile (str): input YAML file to be read
    """
    # Metadata
    print(
        Panel(
            f"""
        Name: {framework['metadata']['name']}
        Description: {framework['metadata']['description']}
        Version: {framework['metadata']['version']}
        Author: {framework['metadata']['author']}
        """,
            title="Metadata",
            title_align="left",
            border_style="blue",
        )
    )

    # Describe Engine
    print(
        Panel(
            f"""
        Tool: {framework['engine']['tool']}
        """,
            title="Engine",
            title_align="left",
            border_style="blue",
        )
    )

    # Describe Targets
    print(
        Panel(
            f"""
        Number of Targets: {len(framework['targets'])}
        Available Targets: {", ".join(str(t) for t in framework['targets'])}
        """,
            title="Targets",
            title_align="left",
            border_style="blue",
        )
    )

    # Describe Alias
    if "aliases" in framework:
        available_aliases = Text()
        for alias in framework["aliases"]:
            if available_aliases:
                available_aliases.append(
                    f"\t\t{alias['name']}: {', '.join(str(t) for t in alias['targets'])}\n"
                )
            else:
                available_aliases.append(
                    f"\t{alias['name']}: {', '.join(str(t) for t in alias['targets'])}\n"
                )

        print(
            Panel(
                f"""
        Number of Aliases: {len(framework['aliases'])}
        Available Aliases:
            {available_aliases}
            """,
                title="Aliases",
                title_align="left",
                border_style="blue",
            )
        )

    # Describe Profiles
    available_profiles = Text()
    for profile in framework["profiles"]:
        if available_profiles:
            available_profiles.append(
                f"\t\t{profile['name']}: {', '.join(str(t) for t in profile['targets'])}\n"
            )
        else:
            available_profiles.append(
                f"\t{profile['name']}: {', '.join(str(t) for t in profile['targets'])}\n"
            )
    print(
        Panel(
            f"""
        Number of Profiles: {len(framework['profiles'])}
        Available Profiles:
            {available_profiles}
        """,
            title="Profiles",
            title_align="left",
            border_style="blue",
        )
    )
