# Functions for running and parsing BLAST results
from camlhmp.utils import execute

BLASTN_COLS = [
    "qseqid",
    "sseqid",
    "pident",
    "qcovs",
    "qlen",
    "slen",
    "length",
    "nident",
    "mismatch",
    "gapopen",
    "qstart",
    "qend",
    "sstart",
    "send",
    "evalue",
    "bitscore",
]


def run_blast(engine: str, subject: str, query: str, min_pident: float, min_coverage: int) -> list:
    """
    Query sequences against a input subject using a specified BLAST+ algorithm.

    Args:
        engine (str): The BLAST engine to use
        subject (str): The subject database (input)
        query (str): The query file (targets)
        min_pident (float): The minimum percent identity to count a hit
        min_coverage (int): The minimum percent coverage to count a hit

    Returns:
        list: The parsed BLAST results, raw blast results, and stderr

    Examples:
        >>> from camlhmp.engines.blast import run_blast
        >>> hits, blast_stdout, blast_stderr = run_blast(
                framework["engine"]["tool"], input_path, targets_path, min_pident, min_coverage
            )
    """
    outfmt = " ".join(BLASTN_COLS)
    cat_type = "zcat" if str(subject).endswith(".gz") else "cat"
    qcov_hsp_perc = f"-qcov_hsp_perc {min_coverage}" if min_coverage else ""
    perc_identity = f"-perc_identity {min_pident}" if min_pident and engine != "tblastn" else ""
    stdout, stderr = execute(
        f"{cat_type} {subject} | {engine} -query {query} -subject - -outfmt '6 {outfmt}' {qcov_hsp_perc} {perc_identity}",
        capture=True,
    )

    # Convert BLAST results to a list of dicts
    results = []
    target_hits = []
    for line in stdout.split("\n"):
        if line == "":
            continue
        cols = line.split("\t")
        results.append(dict(zip(BLASTN_COLS, cols)))
        target_hits.append(cols[0])

    if not results:
        # Create an empty dict if no results are found
        results.append(dict(zip(BLASTN_COLS, ["NO_HITS"] * len(BLASTN_COLS))))

    return [target_hits, results, stderr]


def run_blastn(subject: str, query: str, min_pident: float, min_coverage: int) -> list:
    """
    An alias for `run_blast` which uses `blastn`

    Args:
        subject (str): The subject database (input)
        query (str): The query file (targets)
        min_pident (float): The minimum percent identity to count a hit
        min_coverage (int): The minimum percent coverage to count a hit

    Returns:
        list: The parsed BLAST results, raw blast results, and stderr

    Examples:
        >>> from camlhmp.engines.blast import run_blastn
        >>> hits, blast_stdout, blast_stderr = run_blastn(
                input_path, targets_path, min_pident, min_coverage
            )
    """
    return run_blast("blastn", subject, query, min_pident, min_coverage)


def run_tblastn(subject: str, query: str, min_pident: float, min_coverage: int) -> list:
    """
    An alias for `run_blast` which uses `tblastn`.

    Args:
        subject (str): The subject database (input)
        query (str): The query file (targets)
        min_pident (float): The minimum percent identity to count a hit
        min_coverage (int): The minimum percent coverage to count a hit

    Returns:
        list: The parsed BLAST results, raw blast results, and stderr

    Examples:
        >>> from camlhmp.engines.blast import run_tblastn
        >>> hits, blast_stdout, blast_stderr = run_tblastn(
                input_path, targets_path, min_pident, min_coverage
            )
    """
    return run_blast("tblastn", subject, query, min_pident, min_coverage)
