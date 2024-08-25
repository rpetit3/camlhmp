---
title: camlhmp-blast-thresholds
description: >-
    Determine the specificity thresholds for a set of reference sequences 
---

# `camlhmp-blast-thresholds`

`camlhmp-blast-thresholds` is a command that allows users to determine the specificity
percent identity and coverage thresholds when using BLAST+. This command will start at
100 percent identity and coverage and work its way down until a reference sequence can
no longer be distinguished from other reference sequences.

## Usage

```bash
 Usage: camlhmp-blast-thresholds [OPTIONS]

 🐪 camlhmp-blast-thresholds 🐪 - Determine the specificity thresholds for a set of
 reference sequences

╭─ Options ────────────────────────────────────────────────────────────────────────────╮
│ *  --input         -i  TEXT                           Input file in FASTA format of  │
│                                                       reference sequences            │
│                                                       [required]                     │
│ *  --blast         -b  [blastn|blastp|blastx|tblastn  The blast algorithm to use     │
│                        |tblastx]                      [required]                     │
│    --outdir        -o  PATH                           Directory to write output      │
│                                                       [default:                      │
│                                                       ./camlhmp-blast-thresholds]    │
│    --prefix        -p  TEXT                           Prefix to use for output files │
│                                                       [default: camlhmp]             │
│    --min-pident        INTEGER                        Minimum percent identity to    │
│                                                       test                           │
│                                                       [default: 70]                  │
│    --min-coverage      INTEGER                        Minimum percent coverage to    │
│                                                       test                           │
│                                                       [default: 70]                  │
│    --increment         INTEGER                        The value to increment the     │
│                                                       thresholds by                  │
│                                                       [default: 1]                   │
│    --force                                            Overwrite existing reports     │
│    --verbose                                          Increase the verbosity of      │
│                                                       output                         │
│    --silent                                           Only critical errors will be   │
│                                                       printed                        │
│    --version                                          Print schema and camlhmp       │
│                                                       version                        │
│    --help                                             Show this message and exit.    │
╰──────────────────────────────────────────────────────────────────────────────────────╯
```

## Example Usage

To run `camlhmp-blast-thresholds`, you will need a FASTA file of your reference sequences.
Below is an example of how to run `camlhmp-blast-thresholds` using available test data.

```bash
camlhmp-blast-thresholds \
    --input tests/data/blast/targets/sccmec-partial.fasta \
    --blast blastn

Running camlhmp-blast-thresholds with following parameters:
    --input tests/data/blast/targets/sccmec-partial.fasta
    --blast blastn
    --outdir ./camlhmp-blast-thresholds
    --prefix camlhmp
    --min-pident 70
    --min-coverage 70

Gathering seqeuences from tests/data/blast/targets/sccmec-partial.fasta...
Writing reference seqeuences to ./camlhmp-blast-thresholds/reference_seqs...
Detecting failure for ccrA1
Detected failure for ccrA1 with pident=75 and coverage=100 - ['ccrA1', 'ccrA2']
Detecting failure for ccrA2
Detected failure for ccrA2 with pident=75 and coverage=100 - ['ccrA1', 'ccrA2']
Detecting failure for ccrA3
Detected failure for ccrA3 with pident=75 and coverage=95 - ['ccrA1', 'ccrA3']
Detecting failure for ccrB1
Detecting failure for ccrB2
Detecting failure for ccrB3
Detecting failure for IS1272
Detecting failure for mecI
Detecting failure for mecR1
Detecting failure for mecA
Detecting failure for IS431
Writing results to ./camlhmp-blast-thresholds/camlhmp.tsv...
Final Results...
                                                  Thresholds Detection
┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ reference ┃ pident_failure ┃ coverage_failure ┃ hits        ┃ comment                                                ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ IS1272    │ -              │ -                │ -           │ no detection failures for pident>=70 and coverage>=70  │
│ IS431     │ -              │ -                │ -           │ no detection failures for pident>=70 and coverage>=70  │
│ ccrA1     │ 75             │ 100              │ ccrA1,ccrA2 │ Suspected overlap or containment with another target:  │
│ ccrA2     │ 75             │ 100              │ ccrA1,ccrA2 │ Suspected overlap or containment with another target:  │
│ ccrA3     │ 75             │ 95               │ ccrA1,ccrA3 │                                                        │
│ ccrB1     │ -              │ -                │ -           │ no detection failures for pident>=70 and coverage>=70  │
│ ccrB2     │ -              │ -                │ -           │ no detection failures for pident>=70 and coverage>=70  │
│ ccrB3     │ -              │ -                │ -           │ no detection failures for pident>=70 and coverage>=70  │
│ mecA      │ -              │ -                │ -           │ no detection failures for pident>=70 and coverage>=70  │
│ mecI      │ -              │ -                │ -           │ no detection failures for pident>=70 and coverage>=70  │
│ mecR1     │ -              │ -                │ -           │ no detection failures for pident>=70 and coverage>=70  │
└───────────┴────────────────┴──────────────────┴─────────────┴────────────────────────────────────────────────────────┘
Suggested thresholds for specificity: pident>75 and coverage>95
**NOTE** these are suggestions for a starting point
```

!!! Note
    The final results will suggest a starting point for the specificity thresholds. You should
    still validate these thresholds with your own data. You may also notice that shorter
    sequences are more susceptible to percent identity and longer sequences are more susceptible
    to coverage.

## Output Files

`camlhmp-blast-thresholds` will generate an output directory called `camlhmp-blast-thresholds`
by default and in there will be the individual reference sequences and a final table of 
suggested cutoffs.

| File Name              | Description                                                                             |
|------------------------|-----------------------------------------------------------------------------------------|
| `{PREFIX}.tsv`         | A tab-delimited file the threshold failures (if observed) of each reference sequence    |

### {PREFIX}.tsv

The `{PREFIX}.tsv` file is a tab-delimited file the threshold failures (if observed) of each
reference sequence . The columns are:

| Column           | Description                                                                        |
|------------------|------------------------------------------------------------------------------------|
| reference        | The reference sequence name                                                        |
| pident_failure   | The point at which percent identity no longer differentiated from other sequences  |
| coverage_failure | The point at which coverage identity no longer differentiated from other sequences |
| hits             | The other reference sequences that also had a hit                                  |
| comment          | A small comment about the result                                                   |

Below is an example of the `{PREFIX}.tsv` file:

```tsv
reference	pident_failure	coverage_failure	hits	comment
IS1272	-	-	-	no detection failures for pident>=70 and coverage>=70
IS431	-	-	-	no detection failures for pident>=70 and coverage>=70
ccrA1	75	100	ccrA1,ccrA2	Suspected overlap or containment with another target: 
ccrA2	75	100	ccrA1,ccrA2	Suspected overlap or containment with another target: 
ccrA3	75	95	ccrA1,ccrA3	
ccrB1	-	-	-	no detection failures for pident>=70 and coverage>=70
ccrB2	-	-	-	no detection failures for pident>=70 and coverage>=70
ccrB3	-	-	-	no detection failures for pident>=70 and coverage>=70
mecA	-	-	-	no detection failures for pident>=70 and coverage>=70
mecI	-	-	-	no detection failures for pident>=70 and coverage>=70
mecR1	-	-	-	no detection failures for pident>=70 and coverage>=70
```
