# Functions for running and parsing BLAST results
import csv
import logging

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


def get_blast_target_hits(targets: list, results: dict) -> dict:
    """
    Find the target hits in the BLAST results.

    Args:
        targets (list): The list of target sequences
        results (dict): The BLAST results

    Returns:
        dict: The target hits
    """
    target_hits = {}
    for target in targets:
        target_hits[target] = False
        if target in results:
            target_hits[target] = True

    # Debugging information
    logging.debug("camlhmp.engines.blast.get_blast_target_hits")
    logging.debug(f"Profile Hits: {target_hits}")

    return target_hits


def run_blastn(subject: str, query: str, min_pident: float, min_coverage: int) -> dict:
    """
    Query sequences against a input subject using BLASTN.

    Args:
        subject (str): The subject database
        query (str): The query file
        min_pident (float): The minimum percent identity to count a hit
        min_coverage (int): The minimum percent coverage to count a hit

    Returns:
        dict: The parsed BLAST results
    """
    outfmt = " ".join(BLASTN_COLS)
    cat_type = "zcat" if str(subject).endswith(".gz") else "cat"
    stdout, stderr = execute(
        f"{cat_type} {subject} | blastn -query {query} -subject - -outfmt '6 {outfmt}' -qcov_hsp_perc {min_coverage} -perc_identity {min_pident}",
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
