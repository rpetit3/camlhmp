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
