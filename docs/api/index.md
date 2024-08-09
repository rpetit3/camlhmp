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

| Type      | Module                                    | Function                                                                              | Description                                         |
|-----------|-------------------------------------------|---------------------------------------------------------------------------------------|-----------------------------------------------------|
| Engine    | [camlhmp.engines.blast](engines/blast.md) | [run_blast](engines/blast.md#camlhmp.engines.blast.run_blast)                         | Run BLAST program                                   |
| Engine    | [camlhmp.engines.blast](engines/blast.md) | [run_blast](engines/blast.md#camlhmp.engines.blast.run_blastn)                        | Alias for `run_blast` with `blastn` specified       |
| Engine    | [camlhmp.engines.blast](engines/blast.md) | [run_blast](engines/blast.md#camlhmp.engines.blast.run_tblastn)                       | Alias for `run_blast` with `tblastn` specified      |
| Framework | [camlhmp.framework](framework.md)         | [read_framework](framework.md#camlhmp.framework.read_framework)                       | Read the framework YAML file                        |
| Framework | [camlhmp.framework](framework.md)         | [print_version](framework.md#camlhmp.framework.print_version)                         | Print the version of the framework                  |
| Framework | [camlhmp.framework](framework.md)         | [get_types](framework.md#camlhmp.framework.get_types)                                 | Get the types from the framework                    |
| Framework | [camlhmp.framework](framework.md)         | [check_types](framework.md#camlhmp.framework.check_types)                             | Check the types against the results                 |
| Framework | [camlhmp.framework](framework.md)         | [check_regions](framework.md#camlhmp.framework.check_regions)                         | Check the region types against the results          |
| Parser    | [camlhmp.parsers.blast](parsers/blast.md) | [get_blast_allele_hits](parsers/blast.md#camlhmp.parsers.blast.get_blast_allele_hits) | Parse BLAST output for allele hits                  |
| Parser    | [camlhmp.parsers.blast](parsers/blast.md) | [get_blast_region_hits](parsers/blast.md#camlhmp.parsers.blast.get_blast_region_hits) | Parse BLAST output for region hits                  |
| Parser    | [camlhmp.parsers.blast](parsers/blast.md) | [get_blast_target_hits](parsers/blast.md#camlhmp.parsers.blast.get_blast_target_hits) | Parse BLAST output for target hits                  |
| Utils     | [camlhmp.utils](utils.md)                 | [execute](utils.md#camlhmp.utils.execute)                                             | Execute a command                                   |
| Utils     | [camlhmp.utils](utils.md)                 | [check_dependencies](utils.md#camlhmp.utils.check_dependencies)                       | Check if all dependencies are installed             |
| Utils     | [camlhmp.utils](utils.md)                 | [get_platform](utils.md#camlhmp.utils.get_platform)                                   | Get the platform of the executing machine           |
| Utils     | [camlhmp.utils](utils.md)                 | [validate_file](utils.md#camlhmp.utils.validate_file)                                 | Validate a file exists and not empty                |
| Utils     | [camlhmp.utils](utils.md)                 | [file_exists_error](utils.md#camlhmp.utils.file_exists_error)                         | Determine if a file exists and raise an error       |
| Utils     | [camlhmp.utils](utils.md)                 | [parse_seq](utils.md#camlhmp.utils.parse_seq)                                         | Parse a sequence file containing a single record    |
| Utils     | [camlhmp.utils](utils.md)                 | [parse_seqs](utils.md#camlhmp.utils.parse_seqs)                                       | Parse a sequence file containing a multiple records |
| Utils     | [camlhmp.utils](utils.md)                 | [parse_table](utils.md#camlhmp.utils.parse_table)                                     | Parse a delimited file                              |
| Utils     | [camlhmp.utils](utils.md)                 | [parse_yaml](utils.md#camlhmp.utils.parse_yaml)                                       | Parse a YAML file                                   |
| Utils     | [camlhmp.utils](utils.md)                 | [write_tsv](utils.md#camlhmp.utils.write_tsv)                                         | Write the dictionary to a TSV file                  |
