# camlhmp

🐪 camlhmp 🐪 - Classification through yAML Heuristic Mapping Protocol

`camlhmp` is a tool for generating organism typing tools from YAML schemas. Through discussions
with Tim Read, we identified a need for a straightforward method to define and manage typing
schemas for organisms of interest. YAML was chosen for its simplicity and readability.

## Purpose

The primary purpose of `camlhmp` is to provide a framework that enables researchers to
_independently_ define typing schemas for their organisms of interest using YAML. This
approach facilitates the management and analysis biological data for researchers at any
level of experience.

`camlhmp` does not supply pre-defined typing schemas. Instead, it equips researchers
with the necessary tools to create and maintain their own schemas, ensuring these schemas
can easily remain up to date with the latest scientific developments.

Finally, the development of `camlhmp` was driven by a practical need to streamline
maintenance of multiple organism typing tools. Managing these tools separately is
time-consuming and challenging. `camlhmp` simplifies this by providing a single
framework for each tool.

## Quick Start

To quickly get started with `camlhmp`, you can install it through Bioconda and run the
command-line interface:

```bash
# Install camlhmp through Bioconda
conda create -n camlhmp -c conda-forge -c bioconda camlhmp
conda activate camlhmp
camlhmp --help

# Example usage of camlhmp-blast-alleles
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

For more example commands and outputs, see the documentation for each command:

- [camlhmp-blast-alleles](https://rpetit3.github.io/camlhmp/latest/cli/blast/camlhmp-blast-alleles/)
- [camlhmp-blast-regions](https://rpetit3.github.io/camlhmp/latest/cli/blast/camlhmp-blast-regions/)
- [camlhmp-blast-targets](https://rpetit3.github.io/camlhmp/latest/cli/blast/camlhmp-blast-targets/)

## Documentation Overview

[Installation](installation.md)  
Information for installing `camlhmp` on your system

[Available Tools](available-tools.md)  
A list of available typing tools utilizing `camlhmp`

[Schema Definition](schema.md)  
Details about defining schemas for use with `camlhmp`

[CLI Reference](cli/index.md)  
Details about available CLI commands from `camlhmp`

[API Reference](api/index.md)  
Details about using the `camlhmp` package in your own code

[About](about.md)  
Information about the development and funding of `camlhmp`

## Funding

Support for this project came (in part) from the [Wyoming Public Health Division](https://health.wyo.gov/publichealth/), and
the [Center for Applied Pathogen Epidemiology and Outbreak Control (CAPE)](https://www.linkedin.com/company/center-for-applied-pathogen-epidemiology-and-outbreak-control/).

<a href="https://health.wyo.gov/publichealth/">
![Wyoming Public Health Division](assets/wyphd-banner.jpg){ width="50%" }
</a>
<a href="https://www.linkedin.com/company/center-for-applied-pathogen-epidemiology-and-outbreak-control/">
![Center for Applied 
Pathogen Epidemiology and Outbreak Control](assets/cape-banner.png){ width="40%" }
</a>

## Citing `camlhmp`

If you make use of `camlhmp` in your analysis, please cite the following:

- __camlhmp__  
_Petit III RA, Read TD [camlhmp: Classification through yAML Heuristic Mapping Protocol](https://github.com/rpetit3/camlhmp) (GitHub)_  

- __[BLAST+](https://blast.ncbi.nlm.nih.gov/Blast.cgi)__  
_Camacho C, Coulouris G, Avagyan V, Ma N, Papadopoulos J, Bealer K, Madden TL [BLAST+: architecture and applications](http://dx.doi.org/10.1186/1471-2105-10-421). BMC Bioinformatics 10, 421 (2009)_  
