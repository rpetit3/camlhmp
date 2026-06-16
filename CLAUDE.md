# camlhmp

Classification through yAML Heuristic Mapping Protocol. A Python 3.11+ bioinformatics framework that generates organism typing tools from user-defined YAML schemas. Users describe targets, aliases, and type profiles in YAML; camlhmp runs a configured engine against input sequences and resolves the results into a final type call. The framework is engine-agnostic -- currently BLAST is the only implemented engine, but kmer, phylogenetic, mapping, and other methods are planned. No schemas ship with the package -- they are supplied by the user at runtime.

## Quick Reference

| Task | Command |
|------|---------|
| Install | `just install` (runs `poetry install`) |
| Format | `just fmt` (black + isort) |
| Check formatting | `just check-fmt` |
| Lint | `just lint` (flake8) |
| All checks | `just check` (check-fmt + lint) |
| Build | `just build` (poetry build) |
| Tag a release | `just tag` (prints instructions) |

There is **no test suite**. Test data exists under `tests/data/` but there are no test scripts or pytest configuration.

## Architecture

```
camlhmp/
  __init__.py              # Version via importlib.metadata
  framework.py             # YAML schema I/O, type resolution (get_types, check_types, check_regions)
  utils.py                 # Shell execution (executor lib), file validation, YAML/FASTA/TSV I/O
  engines/                 # Engine implementations (one module per engine type)
    blast.py               # BLAST+ engine: runs via shell pipe (cat/zcat | blastn/tblastn)
  parsers/                 # Result parsers (one module per engine type)
    blast.py               # BLAST parser: allele matching, region coverage, target presence
  visuals/framework.py     # Rich panels for describing a loaded schema
  cli/
    camlhmp.py             # Main entry point -- lists available subcommands
    extract.py             # Extract target sequences from reference genbank/fasta files
    blast/                 # CLI commands for the BLAST engine
      alleles.py           # Per-gene allele classification (exact match vs novel)
      regions.py           # Region-based classification (coverage across multiple HSPs)
      targets.py           # Presence/absence target classification
      thresholds.py        # Iterative threshold sweep to find specificity boundaries
```

New engines follow the same pattern: add a module under `engines/`, a corresponding parser under `parsers/`, and CLI commands under `cli/<engine>/`.

### Data flow (using BLAST engine as example)

1. CLI parses args, loads YAML schema via `framework.read_framework()`
2. Engine runs the analysis (`engines.blast.run_blast()` shells out to BLAST+)
3. Parser aggregates raw output into per-target results (`parsers.blast.get_blast_*_hits()`)
4. `framework.get_types()` resolves aliases into concrete target lists
5. `framework.check_types()` or `check_regions()` matches hits against type profiles
6. Results written as TSV files via `utils.write_tsv()` (result, details, raw output)

## Code Style

- **Formatter**: black (line length 88) + isort
- **Linter**: flake8 (max-line-length 88; ignores E121, E123, E126, E226, E24, E704, W503, W504, E501)
- Run `just check` before committing
- CLI modules use `rich-click` with structured `OPTION_GROUPS` dicts
- Docstrings follow Google-style: Args, Returns, Raises, Examples sections

## Domain Concepts

- **Schema (YAML)**: A user-authored file defining metadata, engine config, targets, aliases, and types. This is the core input that makes camlhmp generic across organisms.
- **Targets**: Named sequence markers (genes, alleles, genomic regions) listed in the schema. Must correspond to sequences in the FASTA targets file.
- **Aliases**: Groups of targets under a single name (e.g., "ccr Type 1" = ccrA1 + ccrB1). Resolved by `get_types()`.
- **Types**: Named profiles that require specific targets/aliases to all be present. Optional `excludes` field causes a type to fail if an excluded target is found.
- **Engine**: The analysis method to use for classification. Configured in the schema's `engine` section with `type` and `tool` fields. Currently only BLAST is implemented (`blastn`, `tblastn`); future engines (k-mer, phylogenetic, mapping, etc.) will follow the same pattern. Default params (`min_pident`, `min_coverage`) can be set in the YAML and overridden on the CLI.
- **Classification modes** (currently BLAST-specific, will generalize as engines are added):
  - `targets` -- binary presence/absence of each target
  - `regions` -- coverage-based; aggregates multiple HSPs to compute percent coverage across a region
  - `alleles` -- allele-level; distinguishes exact known alleles from novel variants

## Environment Setup

Non-Python dependencies (install via conda/mamba):
- `blast` (BLAST+ >= 2.15.0) -- required at runtime for the BLAST engine
- `pigz` -- used for gzip handling
- `just` -- task runner (dev only)

```bash
conda env create -f environment.yml
conda activate camlhmp
just install
```

Environment variables (optional):
- `CAML_YAML` -- default YAML schema path for CLI subcommands
- `CAML_TARGETS` -- default targets FASTA path for CLI subcommands

## Gotchas

- `__init__.py` docstring says "sccmec" (a leftover from the original project this was generalized from). Not a bug, just cosmetic.
- The BLAST engine invokes via shell pipe (`cat file | blastn -subject - ...`), not via makeblastdb. The subject is always streamed from stdin.
- Gzipped inputs are detected by file extension (`.gz`) and decompressed with `zcat` inline.
- The `executor` library is used for shell commands, not `subprocess`. See `utils.execute()`.
- CLI modules check `"--version" in sys.argv` to conditionally mark `--input` as not required. This is a workaround for click's required-option handling.
- Version is managed solely via `pyproject.toml` (`poetry version`); `__init__.py` reads it at runtime via `importlib.metadata`.

## Machine-Readable Index

- [catalog.json](catalog.json): Auto-generated catalog of all commands, API functions, engines, and classification modes. Generated by `.claude/skills/update-catalog/scripts/generate-catalog.py`.
- [llms.txt](llms.txt): AI-discovery surface document for the project.
