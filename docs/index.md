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

## Documentation Overview

[Installation](installation.md)  
Information for installing `camlhmp` on your system

[Available Tools](typers.md)  
A list of available typing tools utilizing `camlhmp`

[Schema Definition](bactopia/gather.md)  
Details about defining schemas for use with `camlhmp`

[API Reference](api/index.md)  
Details about using the `camlhmp` package in your own code

[About](about.md)
Information about the development and funding of `camlhmp`

## Naming

I really wanted to name a tool with "camel" in it because they are my wife's favorite animal🐪
and camels also remind me of my friends in Oman!

Once it was decided YAML was going to be the format for defining schemas, I immediately was
drawn into "Classification through YAML", or _CAML_", but quickly found out many others had
also thought of this (_for other use cases_). We went through a few other iterations of
_CAML_ without any success. Fortunately, Tim Read came through with a clutch save suggested
_"Heuristic Mapping Protocol"_. So, here we are - _camlhmp_!

## Funding

Support for this project came (in part) from the [Wyoming Public Health Division](https://health.wyo.gov/publichealth/), and
the [Center for Applied Pathogen Epidemiology and Outbreak Control (CAPE)](https://www.linkedin.com/company/center-for-applied-pathogen-epidemiology-and-outbreak-control/).

<a href="https://health.wyo.gov/publichealth/">
![Wyoming Public Health Division](assets/wyphd-banner.jpg){ width="50%" }
</a>
<a href="https://www.linkedin.com/company/center-for-applied-pathogen-epidemiology-and-outbreak-control/">
![Center for Applied 
Pathogen Epidemiology and Outbreak Control](assets/cape-banner.png){ width="50%" }
</a>


## Citing `camlhmp`

If you make use of `camlhmp` in your analysis, please cite the following:

- __camlhmp__  
_Petit III RA, Read TD [camlhmp: Classification through yAML Heuristic Mapping Protocol](https://github.com/rpetit3/camlhmp) (GitHub)_  

- __[BLAST+](https://blast.ncbi.nlm.nih.gov/Blast.cgi)__  
_Camacho C, Coulouris G, Avagyan V, Ma N, Papadopoulos J, Bealer K, Madden TL [BLAST+: architecture and applications](http://dx.doi.org/10.1186/1471-2105-10-421). BMC Bioinformatics 10, 421 (2009)_  
