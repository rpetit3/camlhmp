#!/usr/bin/env python3
"""PostToolUse hook: remind to regenerate catalog.json/llms.txt after code edits.

Fires after Edit/Write. If the edited file is package source (camlhmp/**/*.py)
or pyproject.toml, emits a non-blocking reminder to run the `update-catalog`
skill before committing. It never runs the generator itself -- the generator
clobbers in-flight edits, so a reminder preserves the user's review step.
"""
import json
import os
import sys


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return

    file_path = (payload.get("tool_input") or {}).get("file_path", "")
    if not file_path:
        return

    # Match files relative to the repo root so the repo dir also being named
    # "camlhmp" doesn't cause every .py under it to match. Package source lives
    # under the inner camlhmp/ package; pyproject.toml sits at the root.
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    rel = os.path.relpath(file_path, project_dir) if project_dir else ""

    if rel and not rel.startswith(".."):
        is_source = rel.startswith("camlhmp" + os.sep) and rel.endswith(".py")
        is_pyproject = rel == "pyproject.toml"
    else:
        # Fallback when CLAUDE_PROJECT_DIR is unset: match the inner package dir.
        is_source = "/camlhmp/camlhmp/" in file_path and file_path.endswith(".py")
        is_pyproject = file_path.endswith("/pyproject.toml")
    if not (is_source or is_pyproject):
        return

    reminder = (
        "Edited camlhmp package source. catalog.json and llms.txt may now be "
        "stale -- run the `update-catalog` skill before committing if commands, "
        "public functions, or dependencies changed."
    )
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PostToolUse",
                    "additionalContext": reminder,
                }
            }
        )
    )


if __name__ == "__main__":
    main()
