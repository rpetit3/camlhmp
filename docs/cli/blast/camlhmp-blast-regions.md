---
title: camlhmp-blast-regions
description: >-
    Classify assemblies with a camlhmp schema using BLAST against larger genomic regions
---

# `camlhmp-blast-regions`

`camlhmp-blast-regions` is a command that allows users to search for full regions of interest.
It is nearly identical to `camlhmp-blast-targets`, but instead of many smaller targets the
idea is to instead look at full regions such as O-antigens and or similar features.

## Usage

```bash
 Usage: camlhmp-blast-regions [OPTIONS]

 🐪 camlhmp-blast-regions 🐪 - Classify assemblies using BLAST against larger genomic
 regions

╭─ Options ───────────────────────────────────────────────────────────────────────────╮
│ *  --input         -i  TEXT     Input file in FASTA format to classify [required]   │
│ *  --yaml          -y  TEXT     YAML file documenting the targets and types         │
│                                 [required]                                          │
│ *  --targets       -t  TEXT     Query targets in FASTA format [required]            │
│    --outdir        -o  PATH     Directory to write output [default: ./]             │
│    --prefix        -p  TEXT     Prefix to use for output files [default: camlhmp]   │
│    --min-pident        INTEGER  Minimum percent identity to count a hit             │
│                                 [default: 95]                                       │
│    --min-coverage      INTEGER  Minimum percent coverage to count a hit             │
│                                 [default: 95]                                       │
│    --force                      Overwrite existing reports                          │
│    --verbose                    Increase the verbosity of output                    │
│    --silent                     Only critical errors will be printed                │
│    --version                    Print schema and camlhmp version                    │
│    --help                       Show this message and exit.                         │
╰─────────────────────────────────────────────────────────────────────────────────────╯
```

## Example Usage

To run `camlhmp-blast-regions`, you will need a FASTA file of your input sequences, a YAML
file with the schema, and a FASTA file with the targets. Below is an example of how to run
`camlhmp-blast-regions` using available test data.

```bash
# Acquire test data
wget https://raw.githubusercontent.com/rpetit3/camlhmp/refs/heads/main/tests/data/blast/regions/pseudomonas-serogroup.yaml
wget https://raw.githubusercontent.com/rpetit3/camlhmp/refs/heads/main/tests/data/blast/regions/pseudomonas-serogroup.fasta
wget https://github.com/rpetit3/camlhmp/raw/refs/heads/main/tests/data/blast/regions/O1-GCF_000504045.fna.gz

# Run camlhmp-blast-regions
camlhmp-blast-regions \
    --yaml pseudomonas-serogroup.yaml \
    --targets pseudomonas-serogroup.fasta \
    --input O1-GCF_000504045.fna.gz

Running camlhmp-blast-regions with following parameters:
    --input O1-GCF_000504045.fna.gz
    --yaml pseudomonas-serogroup.yaml
    --targets pseudomonas-serogroup.fasta
    --outdir ./
    --prefix camlhmp
    --min-pident 95
    --min-coverage 95

Starting camlhmp for Pseudomonas Serogrouping...
Running blastn...
Processing hits...
Final Results...
                               Pseudomonas Serogrouping
┏━━━━━━━━┳━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┓
┃ sample ┃ type ┃ targe… ┃ cover… ┃ hits ┃ schema ┃ schem… ┃ camlh… ┃ params ┃ comme… ┃
┡━━━━━━━━╇━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━┩
│ camlh… │ O1   │ O1     │ 100.00 │ 1    │ pseud… │ 0.0.1  │ 1.1.4  │ min-c… │        │
└────────┴──────┴────────┴────────┴──────┴────────┴────────┴────────┴────────┴────────┘
Writing outputs...
Final predicted type written to ./camlhmp.tsv
Results against each type written to ./camlhmp.details.tsv
blastn results written to ./camlhmp.blastn.tsv
```

!!! Note
    The table printed to STDOUT by `camlhmp-blast-regions` has been purposefully truncated
    for viewing on the docs. It is the same information that that is in {PREFIX}.tsv.

## Output Files

`camlhmp-blast-region` will generate three output files:

| File Name              | Description                                     |
|------------------------|-------------------------------------------------|
| `{PREFIX}.tsv`         | A tab-delimited file with the predicted type    |
| `{PREFIX}.blast.tsv`   | A tab-delimited file of all blast hits          |
| `{PREFIX}.details.tsv` | A tab-delimited file with details for each type |

### {PREFIX}.tsv

The `{PREFIX}.tsv` file is a tab-delimited file with the predicted type. The columns are:

| Column          | Description                                                        |
|-----------------|--------------------------------------------------------------------|
| sample          | The sample name as determined by `--prefix`                        |
| type            | The predicted type                                                 |
| targets         | The targets for the given type that had a hit                      |
| coverage        | The coverage of the target region                                  |
| hits            | The number of hits used to calculate coverage of the target region |
| schema          | The schema used to determine the type                              |
| schema_version  | The version of the schema used                                     |
| camlhmp_version | The version of camlhmp used                                        |
| params          | The parameters used for the analysis                               |
| comment         | A small comment about the result                                   |

Below is an example of the `{PREFIX}.tsv` file:

```tsv
sample  type    targets coverage        hits    schema  schema_version  camlhmp_version params  comment
camlhmp O1      O1      100.00  1       pseudomonas_serogroup_partial   0.0.1   1.1.4   min-coverage=95;min-pident=95	
```

### {PREFIX}.blast.tsv

The `{PREFIX}.blast.tsv` file is a tab-delimited file of the raw output for all blast hits.
The columns are the standard BLAST output with `-outfmt 6`.

Here is an example of the `{PREFIX}.blast.tsv` file:

```tsv
qseqid  sseqid  pident  qcovs   qlen    slen    length  nident  mismatch        gapopen qstart  qend    sstart  send    evalue  bitscore
O1      NC_023019.1     99.510  100     18368   6580038 18369   18279   87      3       1       18368   1946644 1965010 0.0     33419
O2      NC_023019.1     97.519  15      23303   6580038 1975    1926    47      2       1       1974    1965010 1963037 0.0     3374
O2      NC_023019.1     87.318  15      23303   6580038 1238    1081    122     14      2542    3746    6116835 6118070 0.0     1384
O2      NC_023019.1     96.296  15      23303   6580038 324     312     11      1       22980   23303   1946966 1946644 2.02e-149       531
O2      NC_023019.1     83.417  15      23303   6580038 398     332     43      11      2542    2920    4514276 4514669 2.18e-94        348
O3      NC_023019.1     97.975  11      20210   6580038 1975    1935    38      2       1       1974    1965010 1963037 0.0     3424
O3      NC_023019.1     100.000 11      20210   6580038 292     292     0       0       19919   20210   1946935 1946644 2.91e-152       540
O4      NC_023019.1     95.829  14      15279   6580038 1918    1838    80      0       1       1918    1965010 1963093 0.0     3099
O4      NC_023019.1     99.275  14      15279   6580038 276     274     2       0       15004   15279   1946919 1946644 3.73e-140       499
```

### {PREFIX}.details.tsv

The `{PREFIX}.details.tsv` file is a tab-delimited file with details for each type. This file
can be useful for seeing how a sample did against all other types in a schema.

The columns in this file are:

| Column          | Description                                                        |
|-----------------|--------------------------------------------------------------------|
| sample          | The sample name as determined by `--prefix`                        |
| type            | The predicted type                                                 |
| status          | The status of the type (`True` if passed thresholds, `False` if failed to exceed thresholds) |
| targets         | The targets for the given type that had a match                    |
| missing         | The targets for the given type that were not found                 |
| coverage        | The coverage of the target region                                  |
| hits            | The number of hits used to calculate coverage of the target region |
| schema          | The schema used to determine the type                              |
| schema_version  | The version of the schema used                                     |
| camlhmp_version | The version of camlhmp used                                        |
| params          | The parameters used for the analysis                               |
| comment         | A small comment about the result                                   |

Below is an example of the `{PREFIX}.details.tsv` file:

```tsv
sample  type    status  targets missing coverage        hits    schema  schema_version  camlhmp_version params  comment
camlhmp O1      True    O1              100.00  1       pseudomonas_serogroup_partial   0.0.1   1.1.4   min-coverage=95;min-pident=95
camlhmp O2      False           O2,wzyB 9.86,0.00       2,0     pseudomonas_serogroup_partial   0.0.1   1.1.4   min-coverage=95;min-pident=95   O2:Coverage based on 2 hits
camlhmp O3      False           O3      11.21   2       pseudomonas_serogroup_partial   0.0.1   1.1.4   min-coverage=95;min-pident=95   Coverage based on 2 hits
camlhmp O4      False           O4      14.36   2       pseudomonas_serogroup_partial   0.0.1   1.1.4   min-coverage=95;min-pident=95   Coverage based on 2 hits
camlhmp O5      False           O2      9.86    2       pseudomonas_serogroup_partial   0.0.1   1.1.4   min-coverage=95;min-pident=95   Coverage based on 2 hits
```

## Example Implementation

If you would like to see how `camlhmp-blast-regions` can be used, please see
[pasty](https://github.com/rpetit3/pasty). In `pasty` the schema is set up
to directly use `camlhmp-blast-regions` to classify samples without any extra
logic.

This allows for a simple wrapper like the following:

```bash
#!/usr/bin/env bash
pasty_dir=$(dirname $0)

CAML_YAML="${pasty_dir}/../data/pa-osa.yaml" \
CAML_TARGETS="${pasty_dir}/../data/pa-osa.fasta" \
    camlhmp-blast-regions \
    "${@:1}"
```

This script will run `camlhmp-blast-regions` with the `pasty` schema and targets.
