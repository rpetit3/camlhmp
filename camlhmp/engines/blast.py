# Functions for running and parsing BLAST results
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


def get_blast_region_hits(
    targets: dict, results: dict, min_pident: float, min_coverage: int
) -> dict:
    """
    Aggregate multiple target hits for a region from the BLAST results.

    Args:
        targets (dict): The list of target sequences {id: len(seq)}
        results (list of dict): The BLAST results
        min_pident (float): The minimum percent identity to count a hit
        min_coverage (int): The minimum percent coverage to count a hit

    Returns:
        dict: The target hits
    """
    # Aggregate the hits for each target
    target_results = {}
    for target, length in targets.items():
        target_results[target] = {
            "hits": [],
            "coverage": [0] * length,  # Used to calculate coverage across multiple hits
            "comment": [],
        }

    # Process each blast hit
    for result in results:
        # Only process real hits
        if result["qseqid"] != "NO_HITS":
            # Only keep hits that pass the minimum percent identity
            if float(result["pident"]) >= min_pident:
                # Add hit to list of hits
                target_results[result["qseqid"]]["hits"].append(result)

                # Set the coverage to 1 for each base in the hit
                for i in range(int(result["qstart"]) - 1, int(result["qend"])):
                    target_results[result["qseqid"]]["coverage"][i] += 1

    # Determine coverage for each target
    final_results = {}
    for target, vals in target_results.items():
        final_results[target] = {
            "hits": vals["hits"],
            "coverage": 100
            * (
                sum([1 for i in vals["coverage"] if i > 0])
                / float(len(vals["coverage"]))
            ),
            "comment": [],
        }
        if len(vals["hits"]) > 1:
            final_results[target]["comment"].append(
                f"Coverage based on {len(vals['hits'])} hits"
            )

        if sum([1 for i in vals["coverage"] if i > 1]):
            final_results[target]["comment"].append(
                "There were one or more overlapping hits"
            )

    # Debugging information
    logging.debug("camlhmp.engines.blast_region.get_blast_region_hits")
    logging.debug(f"Profile Hits: {final_results}")

    return final_results


def run_blastn(subject: str, query: str, min_pident: float, min_coverage: int) -> dict:
    """
    Query sequences against a input subject using BLASTN.

    Args:
        subject (str): The subject database (input)
        query (str): The query file (targets)
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
