---
title: camlhmp API Reference
description: >-
    Details about the available API functions in `camlhmp`
---

At it's core `camlhmp` is a library that provides a set of functions for typing organisms. It
includes functions for running programs and parsing their outputs. In situations where the
available CLI commands do not meet your needs, you can use the API functions to build your own
custom workflows.

Currently the following modules are available in the `camlhmp` API:

| Type   | Module                                    | Function                                                                              | Description                                    |
|--------|-------------------------------------------|---------------------------------------------------------------------------------------|------------------------------------------------|
| Engine | [camlhmp.engines.blast](engines/blast.md) | [run_blast](engines/blast.md#camlhmp.engines.blast.run_blast)                         | Run BLAST program                              |
| Engine | [camlhmp.engines.blast](engines/blast.md) | [run_blast](engines/blast.md#camlhmp.engines.blast.run_blastn)                        | Alias for `run_blast` with `blastn` specified  |
| Engine | [camlhmp.engines.blast](engines/blast.md) | [run_blast](engines/blast.md#camlhmp.engines.blast.run_tblastn)                       | Alias for `run_blast` with `tblastn` specified |
| Parser | [camlhmp.parsers.blast](parsers/blast.md) | [get_blast_allele_hits](parsers/blast.md#camlhmp.parsers.blast.get_blast_allele_hits) | Parse BLAST output for allele hits             |
| Parser | [camlhmp.parsers.blast](parsers/blast.md) | [get_blast_region_hits](parsers/blast.md#camlhmp.parsers.blast.get_blast_region_hits) | Parse BLAST output for region hits             |
| parser | [camlhmp.parsers.blast](parsers/blast.md) | [get_blast_target_hits](parsers/blast.md#camlhmp.parsers.blast.get_blast_target_hits) | Parse BLAST output for target hits             |
