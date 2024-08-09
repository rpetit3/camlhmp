# Functions for parsing BLAST results
import logging


def get_blast_allele_hits(
    targets: dict, results: dict, min_pident: float, min_coverage: int
) -> dict:
    """
    Find the allele hits in the BLAST results.

    Args:
        targets (dict): The list of target sequences {id: len(seq)}
        results (list of dict): The BLAST results
        min_pident (float): The minimum percent identity to count a hit
        min_coverage (int): The minimum percent coverage to count a hit

    Returns:
        dict: The allele hits

    Examples:
        >>> from camlhmp.parsers.blast import get_blast_allele_hits
        >>> target_results = get_blast_allele_hits(framework["targets"], blast_stdout, min_pident, min_coverage)
    """
    # Aggregate the hits for each target
    target_results = {}

    for result in results:
        # Only process real hits
        if result["qseqid"] != "NO_HITS":
            target, allele = result["qseqid"].rsplit("_", 1)
            if target not in target_results:
                target_results[target] = {
                    "known": [],
                    "novel": [],
                }

            # only process hits that meet minimum criteria
            if float(result["pident"]) >= min_pident and int(result["qcovs"]) >= min_coverage:
                # hits that meet requirements

                # Default to "NEW" allele, if perfect match use the allele ID
                final_allele = "NEW"
                final_type = "novel"
                if float(result["pident"]) == 100 and int(result["qcovs"]) == 100:
                    final_allele = allele
                    final_type = "known"

                target_results[target][final_type].append({
                        "id": final_allele,
                        "qcovs": result["qcovs"],
                        "pident": float(result["pident"]),
                        "bitscore": result["bitscore"],
                })

    final_allele_hits = {}
    for target in targets:
        final_allele_hits[target] = {
            "id": "-",
            "qcovs": 0,
            "pident": 0,
            "bitscore": 0,
            "comment": "No hits met thresholds",
        }

    for target in target_results:
        if len(target_results[target]["known"]):
            # exact matches to known alleles were found
            if len(target_results[target]["known"]) == 1:
                final_allele_hits[target] = target_results[target]["known"][0]
                final_allele_hits[target]["comment"] = ""
            else:
                # multiple hits
                final_alleles = []
                for hit in target_results[target]["known"]:
                    final_alleles.append(hit["id"])

                final_allele_hits[target] = target_results[target]["known"][0]
                final_allele_hits[target]["id"] = ",".join(final_alleles)
                final_allele_hits[target]["comment"] = "Exact matches to multiple alleles"
        elif len(target_results[target]["novel"]):
            # no exact matches to known alleles were found, but thresholds were met

            # report the top scores
            if len(target_results[target]["novel"]) == 1:
                final_allele_hits[target] = target_results[target]["novel"][0]
                final_allele_hits[target]["comment"] = ""
            else:
                # multiple hits, only report highest score
                final_allele_hits[target] = sorted(target_results[target]["novel"], key=lambda x: x["bitscore"], reverse=True)[0]
                final_allele_hits[target]["comment"] = "No exact matches to known alleles"

    # Debugging information
    logging.debug("camlhmp.engines.blast.get_blast_allele_hits")
    logging.debug(f"Allele Hits: {final_allele_hits}")

    return final_allele_hits


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
    
    Examples:
        >>> from camlhmp.parsers.blast import get_blast_region_hits
        >>> target_results = get_blast_region_hits(target_lengths, blast_stdout, min_pident, min_coverage)
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


def get_blast_target_hits(targets: list, results: dict) -> dict:
    """
    Find the target hits in the BLAST results.

    Args:
        targets (list): The list of target sequences
        results (dict): The BLAST results

    Returns:
        dict: The target hits

    Examples:
        >>> from camlhmp.parsers.blast import get_blast_target_hits
        >>> target_results = get_blast_target_hits(framework["targets"], hits)
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
