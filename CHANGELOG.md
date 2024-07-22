
# Changelog

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
