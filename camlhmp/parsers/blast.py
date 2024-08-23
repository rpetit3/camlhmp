# Functions for parsing BLAST results
import logging

import camlhmp


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


def finalize_regions(prefix: str, hits: dict, framework: dict, min_pident: float, min_coverage: int) -> list:
    """
    Finalize the results from region-based analysis.

    Args:
        prefix (str): The sample prefix
        hits (dict): The BLAST+ results for each target hit
        framework (dict): The framework schema that was used
        min_pident (float): The minimum percent identity to count a hit
        min_coverage (int): The minimum percent coverage to count a hit

    Returns:
        list: The finalized results
    """
    final_type = []
    final_targets = []
    final_coverages = []
    final_hits = []

    # Get a list of targets that met the threshold
    for target, vals in hits.items():
        if vals["status"]:
            final_targets.append(",".join(vals["targets"]))
            final_coverages.append(",".join(vals["coverage"]))
            final_hits.append(",".join(vals["hits"]))

    # Get the final type(s)
    final_details = []
    for type, vals in hits.items():
        final_details.append(
            {
                "sample": prefix,
                "type": type,
                "status": vals["status"],
                "targets": ",".join(vals["targets"]),
                "missing": ",".join(vals["missing"]),
                "coverage": ",".join(vals["coverage"]),
                "hits": ",".join(vals["hits"]),
                "schema": framework["metadata"]["id"],
                "schema_version": framework["metadata"]["version"],
                "camlhmp_version": camlhmp.__version__,
                "params": f"min-coverage={min_coverage};min-pident={min_pident}",
                "comment": ";".join(vals["comment"]),
            }
        )
        if vals["status"]:
            final_type.append(type)

    # Generate a comment based on the results
    comment = ""
    if not len(final_type):
        if len(final_targets):
            comment = "A type could not be determined, but one or more targets found"
        else:
            comment = "A type could not be determined"
    elif len(final_type) > 1:
        comment = f"Found matches for multiple types including: {', '.join(final_type)}"
        final_type = ["multiple"]
    else:
        # There is only one type, capture any available comments
        comment = ";".join(hits[final_type[0]]["comment"])

    # Write final prediction
    final_result = {
        "sample": prefix,
        "type": ",".join(final_type) if len(final_type) > 0 else "-",
        "targets": ",".join(final_targets),
        "coverage": ",".join(final_coverages),
        "hits": ",".join(final_hits),
        "schema": framework["metadata"]["id"],
        "schema_version": framework["metadata"]["version"],
        "camlhmp_version": camlhmp.__version__,
        "params": f"min-coverage={min_coverage};min-pident={min_pident}",
        "comment": comment,
    }

    return final_result, final_details


def finalize_targets(prefix: str, results: dict,  hits: dict, framework: dict, min_pident: float, min_coverage: int) -> list:
    """
    Finalize the target hits.

    Args:
        prefix (str): The sample prefix
        results(dict): The status of each target
        hits (dict): The BLAST+ results for each target hit
        framework (dict): The framework schema that was used
        min_pident (float): The minimum percent identity to count a hit
        min_coverage (int): The minimum percent coverage to count a hit

    Returns:
        list: The finalized target hits

    Examples:
        >>> from camlhmp.parsers.blast import finalize_targets
    """
    final_type = []
    final_targets = []
    final_details = []

    # Get a list of targets that met the threshold
    for target, status in results.items():
        if status:
            final_targets.append(target)

    for type, vals in hits.items():
        final_details.append(
            {
                "sample": prefix,
                "type": type,
                "status": vals["status"],
                "targets": ",".join(vals["targets"]),
                "missing": ",".join(vals["missing"]),
                "schema": framework["metadata"]["id"],
                "schema_version": framework["metadata"]["version"],
                "camlhmp_version": camlhmp.__version__,
                "params": f"min-coverage={min_coverage};min-pident={min_pident}",
                "comment": vals["comment"],
            }
        )
        if vals["status"]:
            final_type.append(type)

    # Generate a comment based on the results
    final_comment = ""
    if not len(final_type):
        if len(final_targets):
            final_comment = "A type could not be determined, but one or more targets found"
        else:
            final_comment = "A type could not be determined"
    elif len(final_type) > 1:
        final_comment = f"Found matches for multiple types including: {', '.join(final_type)}"
        final_type = ["multiple"]

    final_result = {
        "sample": prefix,
        "type": ",".join(final_type) if len(final_type) > 0 else "-",
        "targets": ",".join(final_targets),
        "schema": framework["metadata"]["id"],
        "schema_version": framework["metadata"]["version"],
        "camlhmp_version": camlhmp.__version__,
        "params": f"min-coverage={min_coverage};min-pident={min_pident}",
        "comment": final_comment,
    }

    return final_result, final_details
