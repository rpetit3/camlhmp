---
name: update-catalog
description: Regenerate catalog.json and llms.txt by scanning the camlhmp codebase. Use when asked to update the catalog, rebuild the component index, refresh catalog.json, or sync llms.txt after code changes (new/removed commands, API changes, dependency updates, documentation edits).
---

# Update Catalog

Regenerate the machine-readable component index (`catalog.json`) and the AI-discovery surface (`llms.txt`) by running the self-contained generator script. Both files live at the repo root.

## Steps

1. **Check for uncommitted edits** to `catalog.json` and `llms.txt`:
    ```
    git -C /home/rpetit3/repos/camlhmp status --porcelain catalog.json llms.txt
    ```
    If either file is dirty, show the user the diff and confirm before overwriting. The generator silently clobbers existing output files, so this check is the user's only safety net against losing in-flight edits. If neither file is dirty, proceed directly to Step 2.

2. **Run the generator** to regenerate both files in one invocation:
    ```
    python /home/rpetit3/repos/camlhmp/.claude/skills/update-catalog/scripts/generate-catalog.py \
        --repo-path /home/rpetit3/repos/camlhmp \
        --output /home/rpetit3/repos/camlhmp/catalog.json \
        --llms-output /home/rpetit3/repos/camlhmp/llms.txt \
        --pretty
    ```
    - Always pass `--pretty` so the committed `catalog.json` stays diff-friendly.
    - `--llms-output` triggers `llms.txt` regeneration. Without it, only `catalog.json` is written. Always pass it unless the user explicitly says "catalog only".

3. **Summarize the result.** Show the user:
    - `catalog.json` path and the shape of the change (`git diff --shortstat catalog.json`)
    - `llms.txt` path and whether anything actually changed (`git diff --shortstat llms.txt`)

4. **Do not stage or commit** the updated files. Let the user review the diff first.

## Notes

- **Generator location**: `.claude/skills/update-catalog/scripts/generate-catalog.py`
- **Dependencies**: stdlib only (Python 3.11+ `tomllib`, `ast`, `argparse`, `json`, `re`, `pathlib`). No extra packages needed.
- **`--repo-path` is always `/home/rpetit3/repos/camlhmp`** -- do not guess or prompt.
- **File locations**: `catalog.json` and `llms.txt` both live at the repo root.
- **`llms.txt` is auto-generated** -- if the user wants to change prose structure, they should edit the template string in `generate-catalog.py`, not `llms.txt` directly.
- **What's scanned**: `pyproject.toml` (metadata, entry points, deps), `camlhmp/cli/camlhmp.py` (COMMANDS dict), all Python modules under `camlhmp/` (public functions and docstrings), `docs/available-tools.md` (external tools table).

### CLI Reference (`generate-catalog.py`)

Required:
- `--repo-path PATH` -- root directory of the camlhmp repository

Catalog output:
- `-o, --output PATH` -- where to write `catalog.json` (default: stdout)
- `--pretty` -- pretty-print JSON with 2-space indentation

llms.txt output:
- `--llms-output PATH` -- where to write the rendered `llms.txt`. Omit to skip llms.txt rendering.
