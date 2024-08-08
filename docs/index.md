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
