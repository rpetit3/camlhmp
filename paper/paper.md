---
title: 'camlhmp: A simple framework for building reproducible microbial genome-based typing tools'
tags:
  - bioinformatics
  - microbial typing
  - Pseudomonas aeruginosa
  - Staphylococcus aureus
  - Streptococcus pneumoniae
authors:
  - name: Robert A. Petit III
    orcid: 0000-0002-1350-9426
    affiliation: "1,2"
  - name: Chayse M. Rowley
    affiliation: "1"
  - name: Taylor R. Fearing
    affiliation: "1"
  - name: Stefaan Verwimp
    orcid: 0000-0002-1350-9426
    affiliation: "4"
  - name: Rob G. Christensen
    affiliation: "1"
  - name: Jim A. Mildenberger
    affiliation: "1"
  - name: Joseph M. Reed
    affiliation: "1"
  - name: Timothy D. Read
    orcid: 0000-0001-8966-9680
    affiliation: "2,3"
affiliations:
  - index: 1
    name: Wyoming Public Health Laboratory, Wyoming Department of Health, Cheyenne, Wyoming, USA
  - index: 2
    name: Center of Applied Pathogen Epidemiology and Outbreak Response, Georgia PGCoE, Atlanta, Georgia, USA
  - index: 3
    name: Division of Infectious Diseases, Department of Medicine, Emory University School of Medicine, Atlanta, Georgia, USA
  - index: 4
    name: Computational Systems Biology, Department of Microbial and Molecular Systems, KU Leuven, Belgium
date: 2025-09-16
bibliography: paper.bib
---

# Summary

Sequence-based typing (SBT) is critical for microbial genomics, yet existing tools are often
developed in isolation, leading to duplicated efforts, inconsistent formats, and limited
community participation. Here we present `camlhmp` (Classification through
yAML Heuristic Mapping Protocol; pronounced *"camel hump"*), a flexible framework for
creating, executing, and maintaining SBT tools. To demonstrate its application, we developed
three `camlhmp`\-powered tools for typing *Pseudomonas aeruginosa*, *Staphylococcus aureus*,
and *Streptococcus pneumoniae*. `camlhmp` is available from PyPi, Bioconda, and
at [https://github.com/rpetit3/camlhmp](https://github.com/rpetit3/camlhmp)

# Statement of Need

In microbiology, genetic typing is commonly used to define genotypes and infer phenotypes.
Many assays have been developed for the laboratory using PCR-based NAATs (Nucleic Acid
Amplification Tests) [@Vaneechoutte1997-pm]. However, with the prevalence of whole-genome
sequencing, new bioinformatics-based approaches are increasingly being developed [@Simar2021-bo].
Developing a new SBT tool requires both extensive knowledge of the target organism and
expertise in bioinformatics. These tools are often developed without adhering to standard
practices, hindering community contributions.

Recognizing the need for a standardized framework to develop easy to use and accessible
SBT tools, we developed `camlhmp`. `camlhmp` is a Python-based framework designed to simplify
the development and management of SBT tools. It uses YAML [@yaml-pf], a simple human-readable
data serialization language, to define a typing schema. From the schema, `camlhmp` will produce
genetic typing results for an input genome in a consistent tab-delimited format.

# `camlhmp` Design

The `camlhmp` (v1.1.0) framework consisted of a user-supplied YAML schema and FASTA format
sequence file, a command-line interface (CLI), and an application programming interface (API).

### User-supplied files: YAML and FASTA

The YAML format was selected primarily for its human readability compared to formats such as
JSON [@json-wm] or TOML [@toml-ku]. Each YAML schema was composed of specific sections,
including `metadata`, `engine`, `targets`, `aliases`, and `types`. `metadata` included fields
to describe the schema, such as name and description. `engine` included a description of the
software tool used to compare query sequences to the input genome. `targets` included a list
of all the targets within the schema, each represented in the corresponding reference FASTA
file. `aliases` allowed for a name to represent a group of targets. Finally, `types` defined
each type based on the presence of specified `targets` or `aliases`.

### Command-line interface

`camlhmp` (v1.1.0) included three CLI tools: `camlhmp-blast-alleles`, `camlhmp-blast-regions`,
and `camlhmp-blast-targets`.

Each command expected an `camlhmp` schema and the corresponding target FASTA file, as well as
the FASTA-formatted assembly, to be typed. Each utilized BLAST+ [@Camacho2009-vc]
to align the target sequences to the sample while differing in the type of test
performed. `camlhmp-blast-alleles` expected target alleles for loci to be aligned to, with
alleles assigned by perfect matches. `camlhmp-blast-regions` expected large genomic
regions to be aligned in single or multiple hits, with types assigned based on percent
coverage and fewest hits. `camlhmp-blast-targets` expected individual target sequences
to be aligned with the types assigned based on the group of targets with a match.

### Application programming interface

The `camlhmp` (v1.1.0) API was grouped into the following types: `engine`, `framework`,
`parser`, and `utility`. `engine` included modules for executing bioinformatic tools.
`framework` included modules for working with the `camlhmp` schema files. `parser` included
modules for parsing the outputs from the `engine` modules. Finally, `utility` included
generic modules for reading, writing, and validating data.

# Application of `camlhmp`

To demonstrate the application of `camlhmp`, we developed schemas for the bacterial pathogens
*Pseudomonas aeruginosa*, *Streptococcus pneumoniae*, and *Staphylococcus aureus.*

`pasty` ([https://github.com/rpetit3/pasty](https://github.com/rpetit3/pasty)), for
serogrouping *P. aeruginosa* samples, used `camlhmp-blast-regions` to align user assemblies to
representative O-specific antigen (OSA) clusters [@Thrane2016-ga] to user assemblies.

`pbptyper` ([https://github.com/rpetit3/pbptyper](https://github.com/rpetit3/pbptyper)), for
typing the penicillin-binding protein (PBP) in *S. pneumoniae* [@Chambers1999-dm], used the
`camlhmp` API to align representative PBPs alleles [@Li2016-dy] against user assemblies.

`sccmec` ([https://github.com/rpetit3/sccmec](https://github.com/rpetit3/sccmec)), for typing
SCC*mec* cassette in *S. aureus* samples [@Uehara2022-en], used `camlhmp-blast-targets` to
align user assemblies against known target SCC*mec* [@Wolska-Gebarzewska2023-ig] associated
genes.

Each can be used as stand-alone tools or from the Bactopia pipeline (v3.2.0) [@Petit2020-gt].

# Conclusion

We developed `camlhmp` to address the challenge in microbiology of creating and maintaining
SBT tools that are both standardized and accessible. We used YAML for defining, executing,
and maintaining these tools, lowering the barrier for researchers to develop organism-specific
typing schemas. To demonstrate `camlhmp`'s flexibility, we developed three `camlhmp`\-powered
typing tools: `pasty`, `pbptyper`, and `sccmec`. As genomic surveillance continues to grow,
tools like `camlhmp` will play an essential role in supporting sustainable typing efforts
across diverse microbial pathogens.

# Code Availability

camlhmp is available at GitHub, PyPi, and Bioconda:

- [https://github.com/rpetit3/camlhmp](https://github.com/rpetit3/camlhmp)  
- [https://pypi.org/project/camlhmp/](https://pypi.org/project/camlhmp/)
- [https://bioconda.github.io/recipes/camlhmp/README.html](https://bioconda.github.io/recipes/camlhmp/README.html)

Documentation for camlhmp is available at [https://rpetit3.github.io/camlhmp/](https://rpetit3.github.io/camlhmp/).

`camlhmp`\-powered Typing Tools are available from GitHub, Bioconda, and Bactopia:

- `pasty` \- [https://github.com/rpetit3/pasty](https://github.com/rpetit3/pasty)
- `pbptyper` \- [https://github.com/rpetit3/pbptyper](https://github.com/rpetit3/pbptyper)
- `sccmec` \- [https://github.com/rpetit3/sccmec](https://github.com/rpetit3/sccmec)

# Conflict of Interest

The authors declare no conflict of interest.

# Acknowledgements

RP3 and TDR received support for this work from the Office of Advanced Molecular Detection,
Centers for Disease Control and Prevention (cooperative agreement number CK22-2204 through
contract 40500-050-23234506 from the Georgia Department of Public Health.

# References
