---
title: camlhmp-blast-targets
description: >-
    Classify assemblies using BLAST against individual genes or proteins
---

# `camlhmp-blast-targets`

`camlhmp-blast-targets` is a command that allows users to type their samples using a provided
schema with BLAST algorithms. This command is useful when a schema is looking at full length
genes or proteins.

## Usage

```bash
 Usage: camlhmp-blast-targets [OPTIONS]

 🐪 camlhmp-blast-targets 🐪 - Classify assemblies using BLAST against individual
 genes or proteins

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

To run `camlhmp-blast-targets`, you will need a FASTA file of your input sequences, a YAML
file with the schema, and a FASTA file with the targets. Below is an example of how to run
`camlhmp-blast-targets` using available test data.

```bash
camlhmp-blast-targets \
    --yaml tests/data/blast/targets/sccmec-partial.yaml \
    --targets tests/data/blast/targets/sccmec-partial.fasta \
    --input tests/data/blast/targets/sccmec-i.fasta

Running camlhmp with following parameters:
    --input tests/data/blast/targets/sccmec-i.fasta
    --yaml tests/data/blast/targets/sccmec-partial.yaml
    --targets tests/data/blast/targets/sccmec-partial.fasta
    --outdir ./
    --prefix camlhmp
    --min-pident 95
    --min-coverage 95

Starting camlhmp for SCCmec Typing...
Running blastn...
Processing hits...
Final Results...
                                     SCCmec Typing
┏━━━━━━━━━┳━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━┓
┃ sample  ┃ type ┃ targets   ┃ schema    ┃ schema_v… ┃ camlhmp… ┃ params    ┃ comment ┃
┡━━━━━━━━━╇━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━┩
│ camlhmp │ I    │ ccrA1,cc… │ sccmec_p… │ 0.0.1     │ 0.3.1    │ min-cove… │         │
└─────────┴──────┴───────────┴───────────┴───────────┴──────────┴───────────┴─────────┘
Writing outputs...
Final predicted type written to ./camlhmp.tsv
Results against each type written to ./camlhmp.details.tsv
blastn results written to ./camlhmp.blastn.tsv
```

!!! Note
    The table printed to STDOUT by `camlhmp-blast-targets` has been purposefully truncated
    for viewing on the docs. It is the same information that that is in {PREFIX}.tsv.

## Output Files

`camlhmp-blast-targets` will generate three output files:

| File Name              | Description                                     |
|------------------------|-------------------------------------------------|
| `{PREFIX}.tsv`         | A tab-delimited file with the predicted type    |
| `{PREFIX}.blast.tsv`   | A tab-delimited file of all blast hits          |
| `{PREFIX}.details.tsv` | A tab-delimited file with details for each type |

### {PREFIX}.tsv

The `{PREFIX}.tsv` file is a tab-delimited file with the predicted type. The columns are:

| Column          | Description                                      |
|-----------------|--------------------------------------------------|
| sample          | The sample name as determined by `--prefix`      |
| type            | The predicted type                               |
| targets         | The targets for the given type that had a hit    |
| schema          | The schema used to determine the type            |
| schema_version  | The version of the schema used                   |
| camlhmp_version | The version of camlhmp used                      |
| params          | The parameters used for the analysis             |
| comment         | A small comment about the result                 |

Below is an example of the `{PREFIX}.tsv` file:

```tsv
sample	type	targets	schema	schema_version	camlhmp_version	params	comment
camlhmp	I	ccrA1,ccrB1,IS431,IS1272,mecA,mecR1	sccmec_partial	0.0.1	0.2.1	min-coverage=95;min-pident=95	
```

### {PREFIX}.blast.tsv

The `{PREFIX}.blast.tsv` file is a tab-delimited file of the raw output for all blast hits.
The columns are the standard BLAST output with `-outfmt 6`.

Here is an example of the `{PREFIX}.blast.tsv` file:

```tsv
qseqid	sseqid	pident	qcovs	qlen	slen	length	nident	mismatch	gapopen	qstart	qend	sstart	send	evalue	bitscore
ccrA1	AB033763.2	100.000	100	1350	39332	1350	1350	0	0	1	1350	23692	25041	0.0	2494
ccrB1	AB033763.2	100.000	100	1152	39332	1152	1152	0	0	1	1152	25063	26214	0.0	2128
IS1272	AB033763.2	100.000	100	1659	39332	1659	1659	0	0	1	1659	28423	30081	0.0	3064
mecR1	AB033763.2	100.000	100	987	39332	987	987	0	0	1	987	30304	31290	0.0	1823
mecA	AB033763.2	99.950	100	2007	39332	2007	2006	1	0	1	2007	31390	33396	0.0	3701
mecA	AB033763.2	99.950	100	2007	39332	2007	2006	1	0	1	2007	31390	33396	0.0	3701
IS431	AB033763.2	99.873	100	790	39332	790	789	1	0	1	790	35958	36747	0.0	1454
IS431	AB033763.2	100.000	100	792	39332	792	792	0	0	1	792	35957	36748	0.0	1463
```

### {PREFIX}.details.tsv

The `{PREFIX}.details.tsv` file is a tab-delimited file with details for each type. This file
can be useful for seeing how a sample did against all other types in a schema.

The columns in this file are:

| Column          | Description                                        |
|-----------------|----------------------------------------------------|
| sample          | The sample name as determined by `--prefix`        |
| type            | The predicted type                                 |
| status          | The status of the type (True if failed)            |
| targets         | The targets for the given type that had a match    |
| missing         | The targets for the given type that were not found |
| schema          | The schema used to determine the type              |
| schema_version  | The version of the schema used                     |
| camlhmp_version | The version of camlhmp used                        |
| params          | The parameters used for the analysis               |
| comment         | A small comment about the result                   |

Below is an example of the `{PREFIX}.details.tsv` file:

```tsv
sample	type	status	targets	missing	schema	schema_version	camlhmp_version	params	comment
camlhmp	I	True	ccrA1,ccrB1,IS431,mecA,mecR1,IS1272		sccmec_partial	0.0.1	0.2.1	min-coverage=95;min-pident=95	
camlhmp	II	False	IS431,mecA,mecR1	ccrA2,ccrB2,mecI	sccmec_partial	0.0.1	0.2.1	min-coverage=95;min-pident=95	
camlhmp	III	False	IS431,mecA,mecR1	ccrA3,ccrB3,mecI	sccmec_partial	0.0.1	0.2.1	min-coverage=95;min-pident=95	
camlhmp	IV	False	IS431,mecA,mecR1,IS1272	ccrA2,ccrB2	sccmec_partial	0.0.1	0.2.1	min-coverage=95;min-pident=95	
```

## Example Implementation

If you would like to see how `camlhmp-blast-targets` can be used, please see
[sccmec](https://github.com/rpetit3/sccmec). In `sccmec` the schema is set up
to directly use `camlhmp-blast-targets` to classify samples without any extra
logic.

This allows for a simple wrapper like the following:

```bash
#!/usr/bin/env bash
sccmec_dir=$(dirname $0)

CAML_YAML="${sccmec_dir}/../data/sccmec.yaml" \
CAML_TARGETS="${sccmec_dir}/../data/sccmec.fasta" \
    camlhmp-blast-targets \
    "${@:1}"
```

This script will run `camlhmp-blast-targets` with the `sccmec` schema and targets.
