---
title: camlhmp-blast-targets
description: >-
    Classify assemblies using BLAST against alleles of a set of genes
---

# `camlhmp-blast-alleles`

`camlhmp-blast-alleles` is a command that allows users to type their samples using a provided
schema with BLAST algorithms. This command is useful when the schema is typing specific alleles
of a gene or set of genes (e.g. MLST).

```bash
 Usage: camlhmp-blast-alleles [OPTIONS]

 🐪 camlhmp-blast-alleles 🐪 - Classify assemblies using BLAST against alleles of
 a set of genes

╭─ Options ──────────────────────────────────────────────────────────────────────╮
│ *  --input         -i  TEXT     Input file in FASTA format to classify         │
│                                 [required]                                     │
│ *  --yaml          -y  TEXT     YAML file documenting the targets and types    │
│                                 [required]                                     │
│ *  --targets       -t  TEXT     Query targets in FASTA format [required]       │
│    --outdir        -o  PATH     Directory to write output [default: ./]        │
│    --prefix        -p  TEXT     Prefix to use for output files                 │
│                                 [default: camlhmp]                             │
│    --min-pident        INTEGER  Minimum percent identity to count a hit        │
│                                 [default: 95]                                  │
│    --min-coverage      INTEGER  Minimum percent coverage to count a hit        │
│                                 [default: 95]                                  │
│    --force                      Overwrite existing reports                     │
│    --verbose                    Increase the verbosity of output               │
│    --silent                     Only critical errors will be printed           │
│    --version                    Print schema and camlhmp version               │
│    --help                       Show this message and exit.                    │
╰────────────────────────────────────────────────────────────────────────────────╯
```

## Example Usage

To run `camlhmp-blast-alleles`, you will need a FASTA file of your input sequences, a YAML
file with the schema, and a FASTA file with the targets. Below is an example of how to run
`camlhmp-blast-alleles` using available test data.

```bash
# Acquire test data
wget https://raw.githubusercontent.com/rpetit3/camlhmp/refs/heads/main/tests/data/blast/alleles/spn-pbptype.yaml
wget https://raw.githubusercontent.com/rpetit3/camlhmp/refs/heads/main/tests/data/blast/alleles/spn-pbptype.fasta
wget https://github.com/rpetit3/camlhmp/raw/refs/heads/main/tests/data/blast/alleles/SRR2912551.fna.gz

# Run camlhmp-blast-alleles
camlhmp-blast-alleles \
    --yaml spn-pbptype.yaml \
    --targets spn-pbptype.fasta \
    --input SRR2912551.fna.gz

Running camlhmp-blast-alleless with following parameters:
    --input SRR2912551.fna.gz
    --yaml spn-pbptype.yaml
    --targets spn-pbptype.fasta
    --outdir ./
    --prefix camlhmp
    --min-pident 95
    --min-coverage 95

Starting camlhmp for S. pneumoniae PBP typing...
Running tblastn...
Processing hits...
Final Results...
                               S. pneumoniae PBP typing
┏━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━━┳━━━┳━━━━┳━━━┳━━━━┳━━━┳━━━━┳━━━┳━━━━┳━━━┳━━━━┓
┃ … ┃ … ┃ … ┃ … ┃ … ┃ … ┃ … ┃ … ┃ … ┃ 1… ┃ … ┃ 2… ┃ … ┃ 2… ┃ … ┃ 2… ┃ … ┃ 2… ┃ … ┃ 2… ┃
┡━━━╇━━━╇━━━╇━━━╇━━━╇━━━╇━━━╇━━━╇━━━╇━━━━╇━━━╇━━━━╇━━━╇━━━━╇━━━╇━━━━╇━━━╇━━━━╇━━━╇━━━━┩
│ … │ … │ … │ … │ … │ … │ … │ … │ … │    │ 0 │ 1… │ … │ 5… │   │ 2  │ … │ 1… │ … │    │
└───┴───┴───┴───┴───┴───┴───┴───┴───┴────┴───┴────┴───┴────┴───┴────┴───┴────┴───┴────┘
Writing outputs...
Final predicted type written to ./camlhmp.tsv
tblastn results written to ./camlhmp.tblastn.tsv
```

!!! Note
    The table printed to STDOUT by `camlhmp-blast-alleles` has been purposefully truncated
    for viewing on the docs. It is the same information that that is in {PREFIX}.tsv.

## Output Files

`camlhmp-blast-alleles` will generate three output files:

| File Name              | Description                                     |
|------------------------|-------------------------------------------------|
| `{PREFIX}.tsv`         | A tab-delimited file with the predicted type    |
| `{PREFIX}.blast.tsv`   | A tab-delimited file of all blast hits          |

### {PREFIX}.tsv

The `{PREFIX}.tsv` file is a tab-delimited file with the predicted type. The columns are:

| Column            | Description                                                        |
|-------------------|--------------------------------------------------------------------|
| sample            | The sample name as determined by `--prefix`                        |
| schema            | The schema used to determine the type                              |
| schema_version    | The version of the schema used                                     |
| camlhmp_version   | The version of camlhmp used                                        |
| params            | The parameters used for the analysis                               |
| {TARGET}_id       | The allele ID for a target hit                                     |
| {TARGET}_pident   | The percent identity of the hit                                    |
| {TARGET}_qcovs    | The percent coverage of the hit                                    |
| {TARGET}_bitscore | The bitscore of the hit                                            |
| {TARGET}_comment  | A small comment about the hit                                      |

Below is an example of the `{PREFIX}.tsv` file:

```tsv
sample	schema	schema_version	camlhmp_version	params	1A_id	1A_pident	1A_qcovs	1A_bitscore	1A_comment	2B_id	2B_pident	2B_qcovs	2B_bitscore	2B_comment	2X_id	2X_pident	2X_qcovs	2X_bitscore	2X_comment
camlhmp	pbptype_partial	0.0.1	0.3.1	min-coverage=95;min-pident=95	23	100.0	100	556		0	100.0	100	567		2	100.0	100	741	
```

### {PREFIX}.blast.tsv

The `{PREFIX}.blast.tsv` file is a tab-delimited file of the raw output for all blast hits.
The columns are the standard BLAST output with `-outfmt 6`.

Here is an example of the `{PREFIX}.blast.tsv` file:

```tsv
qseqid	sseqid	pident	qcovs	qlen	slen	length	nident	mismatch	gapopen	qstart	qend	sstart	send	evalue	bitscore
1A_0	NODE_223_length_8196_cov_21.291849	99.638	100	276	8324	276	275	1	0	1	276	1807	2634	0.0	555
1A_1	NODE_223_length_8196_cov_21.291849	99.638	100	276	8324	276	275	1	0	1	276	1807	2634	0.0	555
1A_2	NODE_223_length_8196_cov_21.291849	99.275	100	276	8324	276	274	2	0	1	276	1807	2634	0.0	554
1A_3	NODE_223_length_8196_cov_21.291849	99.275	100	276	8324	276	274	2	0	1	276	1807	2634	0.0	553
1A_4	NODE_223_length_8196_cov_21.291849	84.420	100	276	8324	276	233	43	0	1	276	1807	2634	3.91e-155	474
1A_23	NODE_223_length_8196_cov_21.291849	100.000	100	276	8324	276	276	0	0	1	276	1807	2634	0.0	556
2B_0	NODE_878_length_2854_cov_17.976875	100.000	100	277	2982	277	277	0	0	1	277	1218	2048	0.0	567
2B_1	NODE_878_length_2854_cov_17.976875	87.365	100	277	2982	277	242	35	0	1	277	1218	2048	3.24e-173	501
2B_2	NODE_878_length_2854_cov_17.976875	99.278	100	277	2982	277	275	2	0	1	277	1218	2048	0.0	563
2B_3	NODE_878_length_2854_cov_17.976875	99.639	100	277	2982	277	276	1	0	1	277	1218	2048	0.0	565
2B_4	NODE_878_length_2854_cov_17.976875	99.639	100	277	2982	277	276	1	0	1	277	1218	2048	0.0	565
2X_0	NODE_210_length_5085_cov_16.539627	99.721	100	358	5213	358	357	1	0	1	358	3172	2099	0.0	740
2X_1	NODE_210_length_5085_cov_16.539627	92.179	100	358	5213	358	330	28	0	1	358	3172	2099	0.0	688
2X_1	NODE_878_length_2854_cov_17.976875	23.797	99	358	2982	395	94	230	17	1	353	915	2012	1.95e-06	45.8
2X_2	NODE_210_length_5085_cov_16.539627	100.000	100	358	5213	358	358	0	0	1	358	3172	2099	0.0	741
2X_3	NODE_210_length_5085_cov_16.539627	99.721	100	358	5213	358	357	1	0	1	358	3172	2099	0.0	739
2X_4	NODE_210_length_5085_cov_16.539627	99.441	100	358	5213	358	356	2	0	1	358	3172	2099	0.0	738
```
