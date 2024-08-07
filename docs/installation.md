[![Gitpod ready-to-code](https://img.shields.io/badge/Gitpod-ready--to--code-908a85?logo=gitpod)](https://gitpod.io/#https://github.com/rpetit3/camlhmp)

# camlhmp

🐪 camlhmp 🐪 - Classification through yAML Heuristic Mapping Protocol

`camlhmp` is a tool for generating organism typing tools from YAML schemas. The idea came
up from discussions with Tim Read about the need for a tool that would allow researchers
to more easily define typing schemas for their organisms of interest. YAML seemed like a
a nice format for this due to its simplicity and readability.

_`camlhmp` is under active development, and any feedback is appreciated._

## Purpose

The primary purpose of `camlhmp` is to provide a framework that enables researchers to
independently define typing schemas for their organisms of interest using YAML. This
facilitates the management and analysis biological data, no matter the researchers experience
level.

`camlhmp` does not supply any pre-defined typing schemas. Instead, it provides researchers
with the tools necessary tools to create and maintain their own schemas. This I believe will
ensure the schemas remain up to date with the latest developments in its respective field.

Additionally, this really arose from a practical need to streamline my maintenance of
multiple organism typing tools. Long-term maintenance of these tools is a challenge, and
I think `camlhmp` will help me to keep them up-to-date and consistent.

## Installation

`camlhmp` will be made available through PyPI and Bioconda. For now, you can install it
from the GitHub repository with the following command:

```bash
conda create -n camlhmp -c conda-forge -c bioconda camlhmp
conda activate camlhmp
camlhmp
```

## YAML Schema Structure

The schema structure is designed to be simple and intuitive. Here is a basic skeleton of the
expected schema structure:

```yaml
%YAML 1.2
---
# metadata: general information about the schema
metadata:
  id: ""          # unique identifier for the schema
  name: ""        # name of the schema
  description: "" # description of the schema
  version: ""     # version of the schema
  curators: []    # A list of curators of the schema

# engine: specifies the computational tools and additional parameters used for sequence
#         analysis.
engine:
  tool: "" # The tool used to generate the data

# targets: Lists the specific sequence targets such as genes, proteins, or markers that the
#          schema will analyze. These should be included in the associated sequence query data
targets: []

# aliases: groups multiple targets under a common name for easier reference
aliases:
  - name: ""     # name of the alias
    targets: []  # list of targets that are part of the alias

# types: define specific combinations of targets and aliases to form distinct types
types:
  - name: ""     # name of the profile
    targets: []  # list of targets (can use aliases) that are part of the profile
    excludes: [] # list of targets (or aliases) that will automatically fail the type
```

From this schema we have a few sections:

- `metadata`: general information about the schema
- `engine`: computational requirements for sequence analysis
- `targets`: lists the sequence targets such as genes, proteins, or markers
- `aliases`: groups multiple targets under a common name for easier reference
- `profiles`: defines combinations of targets and aliases to form typing profiles

Within each section there are additional fields that will be descibed in the next sections.

### metadata

The `metadata` section provides general information about the schema. This includes:

| Field        | Type   | Description                                      |
|--------------|--------|--------------------------------------------------|
| id           | string | A unique identifier for the schema               |
| name         | string | The name of the schema                           |
| description  | string | A brief description of the schema                |
| version      | string | The version of the schema                        |
| curators     | list   | A list of curators of the schema                 |

### engine

The `engine` section specifies the computational tools used for sequence analysis. Currently
only one tool can be specified, and only `blastn` is supported.

| Field | Type   | Description                                      |
|-------|--------|--------------------------------------------------|
| tool  | string | The tool used to generate the data               |

### targets

The `targets` section lists the specific sequence targets such as genes, proteins, or markers
that the schema will analyze. These should be included in the associated sequence query data.

| Field   | Type   | Description                                    |
|---------|--------|------------------------------------------------|
| targets | list | A list of targets to be analyzed                 |

### aliases

`aliases` are a convenient way to group multiple targets under a common name for easier
reference.

| Field   | Type   | Description                                    |
|---------|--------|------------------------------------------------|
| name    | string | The name of the alias                          |
| targets | list   | A list of targets that are part of the alias   |

### types

The `types` section defines specific combinations of targets and aliases to form distinct
types.

| Field   | Type   | Description                                                          |
|---------|--------|----------------------------------------------------------------------|
| name    | string | The name of the profile                                              |
| targets | list   | A list of targets (or aliases) that are part of the type             |
| excludes | list  | A list of targets (or aliases) that will automatically fail the type |

### Example Schema: Partial SCCmec Typing

Here is an example of a partial schema for SCCmec typing:

```yaml
%YAML 1.2
---
# metadata: general information about the schema
metadata:
  id: "sccmec_partial"                                # unique identifier for the schema
  name: "SCCmec Typing"                              # name of the schema
  description: "A partial schema for SCCmec typing"  # description of the schema
  version: "0.0.1"                                     # version of the schema
  curators:                                          # A list of curators of the schema
    - "Robert Petit"

# engine: specifies the computational tools and additional parameters used for sequence
#         analysis.
engine:
  tool: blastn # The tool used to generate the data

# targets: Lists the specific sequence targets such as genes, proteins, or markers that the
#          schema will analyze. These should be included in the associated sequence query data
targets:
  - "ccrA1"
  - "ccrA2"
  - "ccrA3"
  - "ccrB1"
  - "ccrB2"
  - "ccrB3"
  - "IS431"
  - "IS1272"
  - "mecA"
  - "mecI"
  - "mecR1"

# aliases: groups multiple targets under a common name for easier reference
aliases:
  - name: "ccr Type 1"           # name of the alias
    targets: ["ccrA1", "ccrB1"]  # list of targets that are part of the alias
  - name: "ccr Type 2"
    targets: ["ccrA2", "ccrB2"]
  - name: "ccr Type 3"
    targets: ["ccrA3", "ccrB3"]
  - name: "mec Class A"
    targets: ["IS431", "mecA", "mecR1", "mecI"]
  - name: "mec Class B"
    targets: ["IS431", "mecA", "mecR1", "IS1272"]

# types: define specific combinations of targets and aliases to form distinct types
types:
  - name: "I"          # name of the profile
    targets:           # list of targets (can use aliases) that are part of the profile
      - "ccr Type 1"
      - "mec Class B"
  - name: "II"
    targets:
      - "ccr Type 2"
      - "mec Class A"
  - name: "III"
    targets:
      - "ccr Type 3"
      - "mec Class A"
  - name: "IV"
    targets:
      - "ccr Type 2"
      - "mec Class B"
```

From this schema, `camlhmp` can generate a typing tool that can be used to analyze input
assemblies. This is only a partial schema, as there are many more SCCmec types and subtypes.
But using this schema it should be straight forward to add additional targets and profiles.

## `camlhmp-blast`

`camlhmp-blast` is a command that allows users to type their samples using a provided schema
with BLAST algorithms.

### Usage

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

### Output Files

`camlhmp-blast` will generate three output files:

| File Name              | Description                                     |
|------------------------|-------------------------------------------------|
| `{PREFIX}.tsv`         | A tab-delimited file with the predicted type    |
| `{PREFIX}.blast.tsv`   | A tab-delimited file of all blast hits          |
| `{PREFIX}.details.tsv` | A tab-delimited file with details for each type |

#### Example {PREFIX}.tsv

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

#### Example {PREFIX}.blast.tsv

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

#### Example {PREFIX}.details.tsv

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

## `camlhmp-blast-region`

`camlhmp-blast-region` is a command that allows users to search for full regions of interest.
It is nearly identical to `camlhmp-blast`, but instead of many smaller targets the idea is to
instead look at full regions such as O-antigens and or similar features.

### Usage

```bash
 Usage: camlhmp-blast-region [OPTIONS]

 🐪 camlhmp-blast-region 🐪 - Classify assemblies with a camlhmp schema using BLAST against
 larger genomic regions

╭─ Options ───────────────────────────────────────────────────────────────────────────────────╮
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
│    --version       -V           Print schema and camlhmp version                            │
│    --help                       Show this message and exit.                                 │
╰─────────────────────────────────────────────────────────────────────────────────────────────╯
```

### Output Files

`camlhmp-blast-region` will generate three output files:

| File Name              | Description                                     |
|------------------------|-------------------------------------------------|
| `{PREFIX}.tsv`         | A tab-delimited file with the predicted type    |
| `{PREFIX}.blast.tsv`   | A tab-delimited file of all blast hits          |
| `{PREFIX}.details.tsv` | A tab-delimited file with details for each type |

#### Example {PREFIX}.tsv

```tsv
sample	type	targets	coverage	hits	schema	schema_version	camlhmp_version	params	comment
camlhmp	O5	O2	100.00	1	pseudomonas_serogroup_partial	0.0.1	0.2.1	min-coverage=95;min-pident=95	

```

| Column  | Description                                      |
|---------|--------------------------------------------------|
| sample  | The sample name as determined by `--prefix`      |
| type    | The predicted type                               |
| targets | The targets for the given type that had a hit    |
| coverage | The coverage of the target region               |
| hits    | The number of hits used to calculate coverage of the target region         |
| schema  | The schema used to determine the type            |
| schema_version  | The version of the schema used           |
| camlhmp_version | The version of camlhmp used              |
| params  | The parameters used for the analysis             |
| comment | A small comment about the result                 |

#### Example {PREFIX}.blast.tsv

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

This is the standard BLAST output with `-outfmt 6`

#### Example {PREFIX}.details.tsv

```tsv
sample	type	status	targets	missing	coverage	hits	schema	schema_version	camlhmp_version	params	comment
camlhmp	O1	False		O1	12.49	2	pseudomonas_serogroup_partial	0.0.1	0.2.1	min-coverage=95;min-pident=95	Coverage based on 2 hits
camlhmp	O2	False	O2	wzyB	100.00,0.00	1,0	pseudomonas_serogroup_partial	0.0.1	0.2.1	min-coverage=95;min-pident=95	
camlhmp	O3	False		O3	1.43	1	pseudomonas_serogroup_partial	0.0.1	0.2.1	min-coverage=95;min-pident=95	
camlhmp	O4	False		O4	13.86	2	pseudomonas_serogroup_partial	0.0.1	0.2.1	min-coverage=95;min-pident=95	Coverage based on 2 hits
camlhmp	O5	True	O2		100.00	1	pseudomonas_serogroup_partial	0.0.1	0.2.1	min-coverage=95;min-pident=95	
```

This file provides a detailed view of the results. The columns are:

| Column  | Description                                        |
|---------|----------------------------------------------------|
| sample  | The sample name as determined by `--prefix`        |
| type    | The predicted type                                 |
| status  | The status of the type (True if failed)            |
| targets | The targets for the given type that had a match    |
| missing | The targets for the given type that were not found |
| coverage | The coverage of the target region                  |
| hits    | The number of hits used to calculate coverage of the target region         |
| schema  | The schema used to determine the type              |
| schema_version  | The version of the schema used             |
| camlhmp_version | The version of camlhmp used                |
| params  | The parameters used for the analysis               |
| comment | A small comment about the result                   |

## `camlhmp-extract`

`camlhmp-extract` is a command that allows users to extract targets from a set of references.
You should think of this script as a "helper" script for curators. It allows you to maintain
a TSV file with the targets and their positions in the reference sequences. `camlhmp-extract`
will then extract the targets from the reference sequences and write them to a FASTA file.

### Usage

```bash
 🐪 camlhmp-extract 🐪 - Extract typing targets from a set of reference sequences

╭─ Required Options ──────────────────────────────────────────────────────────────────────────╮
│ *  --path     -i  TEXT  The path where input files are located [required]                   │
│ *  --targets  -t  TEXT  A TSV of targets to extract in FASTA format [required]              │
╰─────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Additional Options ────────────────────────────────────────────────────────────────────────╮
│ --outdir   -o  TEXT  The path to save the extracted targets                                 │
│ --verbose            Increase the verbosity of output                                       │
│ --silent             Only critical errors will be printed                                   │
│ --version  -V        Show the version and exit.                                             │
│ --help               Show this message and exit.                                            │
╰─────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Citations

If you make use of this tool, please cite the following:

- __camlhmp__  
_Petit III RA [camlhmp: Classification through yAML Heuristic Mapping Protocol](https://github.com/rpetit3/camlhmp) (GitHub)_  

- _[BLAST](https://blast.ncbi.nlm.nih.gov/Blast.cgi)__  
Basic Local Alignment Search Tool  
_Camacho C, Coulouris G, Avagyan V, Ma N, Papadopoulos J, Bealer K, Madden TL [BLAST+: architecture and applications](http://dx.doi.org/10.1186/1471-2105-10-421). BMC Bioinformatics 10, 421 (2009)_  

## Naming

If I'm being honest, I really wanted to name a tool with "camel" in it because they are my
wife's favorite animal🐪 and they also remind me of my friends in Oman!

Once it was decided YAML was going to be the format for defining schemas, I quickly stumbled
on "Classification through YAML" and quickly found out I wasn't the only once who thought
of "CAML". But, no matter, it was decided it would be something with "CAML", then Tim Read
came with the save and suggested "Heuristic Mapping Protocol". So, here we are - _camlhmp_!

## License

I'm not a lawyer and MIT has always been my go-to license. So, MIT it is!
