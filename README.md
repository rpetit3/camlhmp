camlhmp - Classification through yAML Heuristic Mapping Protocol (__yeah, it's a stretch to
make sure 🐪 is in the name!__)

# camlhmp

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

Additionally, this really aroses from a practical need to streamline my maintenance of
multiple organism typing tools. Long-term maintenance of these tools is a challenge, and
I think `camlhmp` will help me to keep them up-to-date and consistent.

## Installation

`camlhmp` will be made available through PyPI and Bioconda. For now, you can install it
from the GitHub repository with the following command:

```bash
conda create -n camlhmp python poetry
conda activate camlhmp
poetry add git+ssh://git@github.com:rpetit3/camlhmp.git
camlhmp --help
```

## YAML Schema Structure

The schema structure is designed to be simple and intuitive. Here is a basic skeleton of the
expected schema structure:

```yaml
%YAML 1.2
---
metadata:
  name: ""
  description: ""
  version: ""
  curators: []

engine:
  tool: ""

targets: []

aliases:
  - name: ""
    targets: []

profiles:
  - name: ""
    targets: []
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

### profiles

The `profiles` section defines specific combinations of targets and aliases to form distinct
typing profiles.

| Field   | Type   | Description                                    |
|---------|--------|------------------------------------------------|
| name    | string | The name of the profile                        |
| targets | list   | A list of targets (can use aliases) that are part of the profile |

### Example Schema: Partial SCCmec Typing

Here is an example of a partial schema for SCCmec typing:

```yaml
%YAML 1.2
---
# metadata: general information about the schema
metadata:
  name: "SCCmec Typing"                              # name of the schema
  description: "A partial schema for SCCmec typing"  # description of the schema
  version: "0.1"                                     # version of the schema
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
# profiles: define specific combinations of targets and aliases to form distinct typing profiles
profiles:
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

## Citations

If you make use of this tool, please cite the following:

* **[BLAST](https://blast.ncbi.nlm.nih.gov/Blast.cgi)**  
Basic Local Alignment Search Tool  
*Camacho C, Coulouris G, Avagyan V, Ma N, Papadopoulos J, Bealer K, Madden TL [BLAST+: architecture and applications](http://dx.doi.org/10.1186/1471-2105-10-421). BMC Bioinformatics 10, 421 (2009)*  

## Naming

If I'm being honest, I really wanted to name a tool with "camel" in it because they are my
wife's favorite animal🐪 and they also remind me of my friends in Oman!

Once it was decided YAML was going to be the format for defining schemas, I quickly stumbled
on "Classification through YAML" and quickly found out I wasn't the only once who thought
of "CAML". But, no matter, it was decided it would be something with "CAML", then Tim Read
came with the save and suggested "Heuristic Mapping Protocol". So, here we are - _camlhmp_!

## License

I'm not a lawyer and MIT has always been my go-to license. So, MIT it is!
