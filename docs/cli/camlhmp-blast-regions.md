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
sample	type	targets	coverage	hits	schema	schema_version	camlhmp_version	params	comment
camlhmp	O5	O2	100.00	1	pseudomonas_serogroup_partial	0.0.1	0.2.1	min-coverage=95;min-pident=95	
```

### {PREFIX}.blast.tsv

The `{PREFIX}.blast.tsv` file is a tab-delimited file of the raw output for all blast hits.
The columns are the standard BLAST output with `-outfmt 6`.

Here is an example of the `{PREFIX}.blast.tsv` file:

```tsv
qseqid	sseqid	pident	qcovs	qlen	slen	length	nident	mismatch	gapopen	qstart	qend	sstart	send	evalue	bitscore
wzyB	NZ_PSQS01000003.1	88.403	99	1140	6935329	595	526	69	0	545	1139	6874509	6875103	0.0	717
wzyB	NZ_PSQS01000003.1	88.403	99	1140	6935329	595	526	69	0	545	1139	6920911	6921505	0.0	717
wzyB	NZ_PSQS01000003.1	89.444	99	1140	6935329	540	483	56	1	1	539	6872864	6873403	0.0	680
wzyB	NZ_PSQS01000003.1	89.444	99	1140	6935329	540	483	56	1	1	539	6919266	6919805	0.0	680
O1	NZ_PSQS01000003.1	97.972	12	18368	6935329	1972	1932	38	2	16398	18368	6620589	6618619	0.0	3419
O1	NZ_PSQS01000003.1	96.296	12	18368	6935329	324	312	11	1	1	323	6641914	6641591	1.68e-149	531
O2	NZ_PSQS01000003.1	99.841	100	23303	6935329	23303	23266	30	1	1	23303	6618619	6641914	0.0	42821
O2	NZ_PSQS01000003.1	86.935	100	23303	6935329	1240	1078	130	12	2542	3749	3864567	3863328	0.0	1363
O3	NZ_PSQS01000003.1	94.442	13	20210	6935329	2393	2260	114	15	1	2386	6618619	6620999	0.0	3664
O3	NZ_PSQS01000003.1	99.308	13	20210	6935329	289	287	2	0	19922	20210	6641626	6641914	3.09e-147	523
O4	NZ_PSQS01000003.1	97.448	14	15279	6935329	1842	1795	47	0	1	1842	6618619	6620460	0.0	3142
O4	NZ_PSQS01000003.1	99.638	14	15279	6935329	276	275	1	0	15004	15279	6641639	6641914	8.46e-142	505
```

### {PREFIX}.details.tsv

The `{PREFIX}.details.tsv` file is a tab-delimited file with details for each type. This file
can be useful for seeing how a sample did against all other types in a schema.

The columns in this file are:

| Column          | Description                                                        |
|-----------------|--------------------------------------------------------------------|
| sample          | The sample name as determined by `--prefix`                        |
| type            | The predicted type                                                 |
| status          | The status of the type (True if failed)                            |
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
sample	type	status	targets	missing	coverage	hits	schema	schema_version	camlhmp_version	params	comment
camlhmp	O1	False		O1	12.49	2	pseudomonas_serogroup_partial	0.0.1	0.2.1	min-coverage=95;min-pident=95	Coverage based on 2 hits
camlhmp	O2	False	O2	wzyB	100.00,0.00	1,0	pseudomonas_serogroup_partial	0.0.1	0.2.1	min-coverage=95;min-pident=95	
camlhmp	O3	False		O3	1.43	1	pseudomonas_serogroup_partial	0.0.1	0.2.1	min-coverage=95;min-pident=95	
camlhmp	O4	False		O4	13.86	2	pseudomonas_serogroup_partial	0.0.1	0.2.1	min-coverage=95;min-pident=95	Coverage based on 2 hits
camlhmp	O5	True	O2		100.00	1	pseudomonas_serogroup_partial	0.0.1	0.2.1	min-coverage=95;min-pident=95	
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
