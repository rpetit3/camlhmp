#!/usr/bin/env python3
"""Generate catalog.json and llms.txt for the camlhmp repository.

Scans pyproject.toml, Python source modules, and documentation to produce
a machine-readable component index and an AI-discovery surface document.

Dependencies: Python 3.11+ stdlib only (tomllib, ast, json, re, pathlib).
"""
import argparse
import ast
import json
import re
import sys
import tomllib
from datetime import datetime, timezone
from pathlib import Path


def parse_pyproject(repo: Path) -> dict:
    """Extract metadata, entry points, and dependencies from pyproject.toml."""
    with open(repo / "pyproject.toml", "rb") as f:
        data = tomllib.load(f)

    poetry = data.get("tool", {}).get("poetry", {})
    return {
        "name": poetry.get("name", ""),
        "version": poetry.get("version", ""),
        "description": poetry.get("description", ""),
        "license": poetry.get("license", ""),
        "homepage": poetry.get("homepage", ""),
        "repository": poetry.get("repository", ""),
        "keywords": poetry.get("keywords", []),
        "python": poetry.get("dependencies", {}).get("python", ""),
        "scripts": poetry.get("scripts", {}),
        "dependencies": {
            k: v
            for k, v in poetry.get("dependencies", {}).items()
            if k != "python"
        },
    }


def extract_commands(repo: Path) -> dict:
    """Extract the COMMANDS dict from camlhmp/cli/camlhmp.py via AST."""
    source = (repo / "camlhmp" / "cli" / "camlhmp.py").read_text()
    tree = ast.parse(source)

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "COMMANDS":
                    return ast.literal_eval(node.value)
    return {}


def extract_module_api(filepath: Path) -> list:
    """Extract public functions with their docstrings and args from a module."""
    if not filepath.exists():
        return []

    source = filepath.read_text()
    tree = ast.parse(source)

    functions = []
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
            sig_args = [arg.arg for arg in node.args.args]
            docstring = ast.get_docstring(node) or ""
            first_line = docstring.split("\n")[0].strip() if docstring else ""

            functions.append(
                {
                    "name": node.name,
                    "args": sig_args,
                    "description": first_line,
                }
            )

    return functions


def extract_available_tools(repo: Path) -> list:
    """Parse the available-tools.md table for external tools built with camlhmp."""
    tools_file = repo / "docs" / "available-tools.md"
    if not tools_file.exists():
        return []

    content = tools_file.read_text()
    tools = []

    for match in re.finditer(
        r"\|\s*\[([^\]]+)\]\(([^)]+)\)\s*\|\s*_([^_]+)_\s*\|\s*([^|]+)\|",
        content,
    ):
        tools.append(
            {
                "name": match.group(1).strip(),
                "url": match.group(2).strip(),
                "organism": match.group(3).strip(),
                "description": match.group(4).strip(),
            }
        )

    return tools


def classify_command(name: str) -> str:
    """Determine the classification mode from a command name."""
    if "alleles" in name:
        return "alleles"
    elif "regions" in name:
        return "regions"
    elif "targets" in name:
        return "targets"
    elif "thresholds" in name:
        return "thresholds"
    elif "extract" in name:
        return "extract"
    return "general"


def build_catalog(repo: Path) -> dict:
    """Build the complete catalog dictionary."""
    pyproject = parse_pyproject(repo)
    commands_dict = extract_commands(repo)

    commands = {}
    for script_name, entry_point in pyproject["scripts"].items():
        commands[script_name] = {
            "description": commands_dict.get(script_name, ""),
            "entry_point": entry_point,
            "classification_mode": classify_command(script_name),
        }

    api_modules = {
        "framework": "camlhmp/framework.py",
        "engines.blast": "camlhmp/engines/blast.py",
        "parsers.blast": "camlhmp/parsers/blast.py",
        "utils": "camlhmp/utils.py",
        "visuals.framework": "camlhmp/visuals/framework.py",
    }

    api = {}
    for module_key, rel_path in api_modules.items():
        funcs = extract_module_api(repo / rel_path)
        if funcs:
            api[module_key] = {
                "module": "camlhmp." + module_key,
                "path": rel_path,
                "functions": funcs,
            }

    return {
        "version": "1.0",
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "camlhmp_version": pyproject["version"],
        "project": {
            "name": pyproject["name"],
            "description": pyproject["description"],
            "license": pyproject["license"],
            "homepage": pyproject["homepage"],
            "repository": pyproject["repository"],
            "keywords": pyproject["keywords"],
            "python": pyproject["python"],
        },
        "dependencies": pyproject["dependencies"],
        "commands": commands,
        "api": api,
        "engines": {
            "blast": {
                "tools": ["blastn", "tblastn"],
                "description": "BLAST+ sequence search via shell pipe",
            }
        },
        "classification_modes": {
            "alleles": "Per-gene allele classification (exact match vs novel variant)",
            "regions": "Coverage-based classification aggregating multiple HSPs across a region",
            "targets": "Binary presence/absence of individual gene or protein targets",
        },
        "schema_structure": {
            "metadata": {
                "fields": ["id", "name", "description", "version", "curators"],
                "description": "General information about the typing schema",
            },
            "engine": {
                "fields": ["type", "tool", "params"],
                "params": ["min_pident", "min_coverage"],
                "description": "Computational tool and default parameters for analysis",
            },
            "targets": {
                "description": "List of sequence targets (genes, proteins, markers) to analyze",
            },
            "aliases": {
                "fields": ["name", "targets"],
                "description": "Groups of targets under a common name for easier reference",
            },
            "types": {
                "fields": ["name", "targets", "excludes"],
                "description": "Combinations of targets/aliases that define distinct types",
            },
        },
        "available_tools": extract_available_tools(repo),
    }


def render_llms_txt(catalog: dict) -> str:
    """Render the llms.txt AI-discovery document from catalog data."""
    lines = []

    lines.append(f"# {catalog['project']['name']}")
    lines.append("")
    lines.append(f"> {catalog['project']['description']}")
    lines.append("")
    lines.append(
        "camlhmp is a framework for generating organism typing tools from YAML schemas."
    )
    lines.append(
        "Researchers define typing schemas (targets, aliases, types) in YAML; camlhmp"
    )
    lines.append(
        "runs BLAST+ against input FASTA assemblies and resolves the results into a"
    )
    lines.append(
        "final type call. No schemas ship with the package -- they are user-supplied."
    )
    lines.append("")

    lines.append("## Core Entry Points")
    lines.append("")
    lines.append(
        "- [pyproject.toml](pyproject.toml): Package metadata, entry points, dependencies"
    )
    lines.append(
        "- [camlhmp/cli/camlhmp.py](camlhmp/cli/camlhmp.py): Main CLI dispatcher"
    )
    lines.append(
        "- [camlhmp/framework.py](camlhmp/framework.py): Schema parsing, type resolution"
    )
    lines.append(
        "- [camlhmp/engines/blast.py](camlhmp/engines/blast.py): BLAST+ execution engine"
    )
    lines.append("")

    lines.append("## CLI Commands")
    lines.append("")
    for name, info in catalog["commands"].items():
        desc = info["description"] or info["entry_point"]
        lines.append(f"- `{name}`: {desc}")
    lines.append("")

    lines.append("## Classification Modes")
    lines.append("")
    for mode, desc in catalog["classification_modes"].items():
        lines.append(f"- **{mode}**: {desc}")
    lines.append("")

    lines.append("## Python API")
    lines.append("")
    for module_key, info in catalog["api"].items():
        func_names = [f["name"] for f in info["functions"]]
        lines.append(
            f"- [{info['path']}]({info['path']}): "
            f"`{'`, `'.join(func_names)}`"
        )
    lines.append("")

    lines.append("## Schema Structure")
    lines.append("")
    lines.append("Typing schemas are YAML files with these sections:")
    for section, info in catalog["schema_structure"].items():
        lines.append(f"- **{section}**: {info['description']}")
    lines.append("")
    lines.append(
        "- [docs/schema.md](docs/schema.md): Full schema specification and examples"
    )
    lines.append("")

    if catalog["available_tools"]:
        lines.append("## Tools Built with camlhmp")
        lines.append("")
        for tool in catalog["available_tools"]:
            lines.append(
                f"- [{tool['name']}]({tool['url']}): "
                f"{tool['description']} (_{tool['organism']}_)"
            )
        lines.append("")

    lines.append("## Documentation")
    lines.append("")
    lines.append("- [README.md](README.md): Project overview and quick start")
    lines.append("- [CHANGELOG.md](CHANGELOG.md): Version history")
    lines.append("- [docs/](docs/): Full MkDocs documentation source")
    lines.append(
        "- [docs/cli/](docs/cli/): CLI command reference (one page per command)"
    )
    lines.append("- [docs/api/](docs/api/): Python API reference")
    lines.append("")

    lines.append("## AI Agent Documentation")
    lines.append("")
    lines.append(
        "- [CLAUDE.md](CLAUDE.md): Project context for AI agents -- "
        "architecture, conventions, gotchas"
    )
    lines.append(
        "- [catalog.json](catalog.json): Machine-readable component index "
        "(this file's structured counterpart)"
    )
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generate catalog.json and llms.txt for camlhmp"
    )
    parser.add_argument(
        "--repo-path",
        type=Path,
        required=True,
        help="Root directory of the camlhmp repository",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Where to write catalog.json (default: stdout)",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON with 2-space indentation",
    )
    parser.add_argument(
        "--llms-output",
        type=Path,
        default=None,
        help="Where to write llms.txt (omit to skip)",
    )

    args = parser.parse_args()
    repo = args.repo_path.resolve()

    if not (repo / "pyproject.toml").exists():
        print(f"ERROR: {repo}/pyproject.toml not found.", file=sys.stderr)
        sys.exit(1)

    catalog = build_catalog(repo)

    indent = 2 if args.pretty else None
    catalog_json = json.dumps(catalog, indent=indent, ensure_ascii=False)

    if args.output:
        args.output.write_text(catalog_json + "\n")
        print(f"Wrote {args.output}", file=sys.stderr)
    else:
        print(catalog_json)

    if args.llms_output:
        llms_txt = render_llms_txt(catalog)
        args.llms_output.write_text(llms_txt)
        print(f"Wrote {args.llms_output}", file=sys.stderr)


if __name__ == "__main__":
    main()
