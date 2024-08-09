[![Gitpod ready-to-code](https://img.shields.io/badge/Gitpod-ready--to--code-908a85?logo=gitpod)](https://gitpod.io/#https://github.com/rpetit3/camlhmp)

# camlhmp

🐪 camlhmp 🐪 - Classification through yAML Heuristic Mapping Protocol

`camlhmp` is a tool for generating organism typing tools from YAML schemas. Through discussions
with Tim Read, we identified a need for a straightforward method to define and manage typing
schemas for organisms of interest. YAML was chosen for its simplicity and readability.

Full documentation for `camlhmp` can be found at [https://rpetit3.github.io/camlhmp/](https://rpetit3.github.io/camlhmp/).

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

## Installation

`camlhmp` is available through [PyPI](https://pypi.org/project/camlhmp/) and
[Bioconda](https://bioconda.github.io/recipes/camlhmp/README.html). While you can install it
through PyPi, it is recommended to install it through BioConda so that non-Python dependencies
are also installed.

```bash
conda create -n camlhmp -c conda-forge -c bioconda camlhmp
conda activate camlhmp
camlhmp
```

## Citing `camlhmp`

If you make use of `camlhmp` in your analysis, please cite the following:

- __camlhmp__  
_Petit III RA, Read TD [camlhmp: Classification through yAML Heuristic Mapping Protocol](https://github.com/rpetit3/camlhmp) (GitHub)_  

- __[BLAST+](https://blast.ncbi.nlm.nih.gov/Blast.cgi)__  
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

## Funding

Support for this project came (in part) from the [Wyoming Public Health Division](https://health.wyo.gov/publichealth/), and
the [Center for Applied Pathogen Epidemiology and Outbreak Control (CAPE)](https://www.linkedin.com/company/center-for-applied-pathogen-epidemiology-and-outbreak-control/).

![Wyoming Public Health Division](docs/assets/wyphd-banner.jpg)
![Center for Applied Pathogen Epidemiology and Outbreak Control](docs/assets/cape-banner.png)
