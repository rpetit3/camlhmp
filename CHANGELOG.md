
# Changelog

## v1.0.1 rpetit3/camlhmp "" 2024/08/??

### `Added`

- `camlhmp-blast-thresholds` command to suggest specificity thresholds for BLAST results
- `print_versions` to print versions from multiple schemas
- `print_camlhmp_version` to print the camlhmp version

## v1.0.0 rpetit3/camlhmp "Dromedary" 2024/08/15

### `Added`

- Added a mkdocs documentation site

### `Fixed`

- fixed `camlhmp-blast-regions` unnecessary debug output
- fixed test schemas to match the new schema format

## v0.3.1 rpetit3/camlhmp "Maybe a cat?" 2024/08/05

### `Fixed`

- `camlhmp-blast-alleles` not having a default value for targets

## v0.3.0 rpetit3/camlhmp "More bunnies and fewer baby birds" 2024/08/05

### `Added`

- `camlhmp-blast-alleles` command to search alleles in a set of query sequences using BLAST algorithms

## v0.2.2 rpetit3/camlhmp "Even a few baby birds" 2024/07/22

### `Fixed`

- `--version` flag now works as expected

## v0.2.1 rpetit3/camlhmp "And a bunch of birds" 2024/07/22

### `Added`

- version output with schema name and version

### `Fixed`

- Empty input files will no longer be processed

## v0.2.0 rpetit3/camlhmp "Four little bunnies" 2024/07/22

### `Added`

- `camlhmp-blast-region` command to search full regions of interest using BLAST algorithms
- added `camlhmp_version`, `schema_version`, and `params` to output files

## v0.1.0 rpetit3/camlhmp "Little baby legs" 2024/04/30

### `Added`

- `camlhmp` command to list all available commands
- `camlhmp-blast` command to search for targets in a set of query sequences using BLAST algorithms
- `camlhmp-extract` command to extract targets from a set of reference sequences
- `excludes` field to `types` section to allow for exclusion of targets from a profile
- replaced `profiles` section with `types` section to better reflect the schema structure
- output of results for `camlhmp-blast`

## v0.0.1 rpetit3/camlhmp "Not even walking yet" 2024/04/24

This is a development release for getting things on PyPi and Bioconda. Not expected to be stable.

## `Added`

- basics of camlhmp with a working example using partial SCCmec
