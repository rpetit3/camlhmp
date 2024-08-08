---
title: camlhmp-blast-targets
description: >-
    Classify assemblies using BLAST against alleles of a set of genes
---

# `camlhmp-blast-targets`

`camlhmp-blast` is a command that allows users to type their samples using a provided schema
with BLAST algorithms.

## Usage

```bash
 🐪 camlhmp-blast 🐪 - Classify assemblies with a camlhmp schema using BLAST                          

╭─ Options ───────────────────────────────────────────────────────────────────────────────────╮
│    --version       -V           Show the version and exit.                                  │
│ *  --input         -i  TEXT     Input file in FASTA format to classify [required]           │
│ *  --yaml          -y  TEXT     YAML file documenting the targets and types [required]      │
│ *  --targets       -t  TEXT     Query targets in FASTA format [required]                    │
│    --outdir        -o  PATH     Directory to write output [default: ./]                     │
│    --prefix        -p  TEXT     Prefix to use for output files [default: camlhmp]           │
│    --min-pident        INTEGER  Minimum percent identity to count a hit [default: 95]       │
│    --min-coverage      INTEGER  Minimum percent coverage to count a hit [default: 95]       │
│    --force                      Overwrite existing reports                                  │
│    --verbose                    Increase the verbosity of output                            │
│    --silent                     Only critical errors will be printed                        │
│    --help                       Show this message and exit.                                 |
╰─────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Output Files

`camlhmp-blast` will generate three output files:

| File Name              | Description                                     |
|------------------------|-------------------------------------------------|
| `{PREFIX}.tsv`         | A tab-delimited file with the predicted type    |
| `{PREFIX}.blast.tsv`   | A tab-delimited file of all blast hits          |
| `{PREFIX}.details.tsv` | A tab-delimited file with details for each type |

### Example {PREFIX}.tsv

```tsv
sample	type	targets	schema	schema_version	camlhmp_version	params	comment
camlhmp	I	ccrA1,ccrB1,IS431,IS1272,mecA,mecR1	sccmec_partial	0.0.1	0.2.1	min-coverage=95;min-pident=95	
```

| Column  | Description                                      |
|---------|--------------------------------------------------|
| sample  | The sample name as determined by `--prefix`      |
| type    | The predicted type                               |
| targets | The targets for the given type that had a hit    |
| schema  | The schema used to determine the type            |
| schema_version  | The version of the schema used           |
| camlhmp_version | The version of camlhmp used              |
| params  | The parameters used for the analysis             |
| comment | A small comment about the result                 |

### Example {PREFIX}.blast.tsv

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

This is the standard BLAST output with `-outfmt 6`

### Example {PREFIX}.details.tsv

```tsv
sample	type	status	targets	missing	schema	schema_version	camlhmp_version	params	comment
camlhmp	I	True	ccrA1,ccrB1,IS431,mecA,mecR1,IS1272		sccmec_partial	0.0.1	0.2.1	min-coverage=95;min-pident=95	
camlhmp	II	False	IS431,mecA,mecR1	ccrA2,ccrB2,mecI	sccmec_partial	0.0.1	0.2.1	min-coverage=95;min-pident=95	
camlhmp	III	False	IS431,mecA,mecR1	ccrA3,ccrB3,mecI	sccmec_partial	0.0.1	0.2.1	min-coverage=95;min-pident=95	
camlhmp	IV	False	IS431,mecA,mecR1,IS1272	ccrA2,ccrB2	sccmec_partial	0.0.1	0.2.1	min-coverage=95;min-pident=95	
```

This file provides a detailed view of the results. The columns are:

| Column  | Description                                        |
|---------|----------------------------------------------------|
| sample  | The sample name as determined by `--prefix`        |
| type    | The predicted type                                 |
| status  | The status of the type (True if failed)            |
| targets | The targets for the given type that had a match    |
| missing | The targets for the given type that were not found |
| schema  | The schema used to determine the type              |
| schema_version  | The version of the schema used             |
| camlhmp_version | The version of camlhmp used                |
| params  | The parameters used for the analysis               |
| comment | A small comment about the result                   |
