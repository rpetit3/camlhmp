---
title: Schema Reference
description: >-
    Details about defining schemas for use with `camlhmp`
---

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
  type: ""            # The type of tool used to generate the data
  tool: ""            # The tool used to generate the data
  params: {}          # Additional parameters for the tool
    min_pident: int   # Minimum percent identity for the tool
    min_coverage: int # Minimum percent coverage for the tool

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

## metadata

The `metadata` section provides general information about the schema. This includes:

| Field        | Type   | Description                                      |
|--------------|--------|--------------------------------------------------|
| id           | string | A unique identifier for the schema               |
| name         | string | The name of the schema                           |
| description  | string | A brief description of the schema                |
| version      | string | The version of the schema                        |
| curators     | list   | A list of curators of the schema                 |

## engine

The `engine` section specifies the computational tools used for sequence analysis.

| Field  | Type   | Description                                          |
|--------|--------|------------------------------------------------------|
| type   | string | The type of engine used for analysis                 |
| tool   | string | The specific tool to be used for the engine          |
| params | dict   | Additional parameters for the tool to use as default |

## targets

The `targets` section lists the specific sequence targets such as genes, proteins, or markers
that the schema will analyze. These should be included in the associated sequence query data.

| Field   | Type   | Description                                    |
|---------|--------|------------------------------------------------|
| targets | list | A list of targets to be analyzed                 |

## aliases

`aliases` are a convenient way to group multiple targets under a common name for easier
reference.

| Field   | Type   | Description                                    |
|---------|--------|------------------------------------------------|
| name    | string | The name of the alias                          |
| targets | list   | A list of targets that are part of the alias   |

## types

The `types` section defines specific combinations of targets and aliases to form distinct
types.

| Field   | Type   | Description                                                          |
|---------|--------|----------------------------------------------------------------------|
| name    | string | The name of the profile                                              |
| targets | list   | A list of targets (or aliases) that are part of the type             |
| excludes | list  | A list of targets (or aliases) that will automatically fail the type |

## Example Schema: Partial SCCmec Typing

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
  type: blast   # The type of tool used to generate the data
  tool: blastn  # The tool used to generate the data
  params:       # Additional parameters for the tool
    min_pident: 80   # Minimum percent identity for the tool
    min_coverage: 80 # Minimum percent coverage for the tool

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
