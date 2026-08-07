"""
Clue definitions – structured clue types for the Griductive game.

Supported core clue types:
  FACT, SAME, DIFFERENT, EXACTLY, AT_LEAST, AT_MOST

Extension clue types:
  NEIGHBOR_COUNT, DIAGONAL

This module provides:
  - Clue type constants
  - Clue validation
  - Direct semantic evaluators (check clue truth without CNF)
"""

from __future__ import annotations

from typing import Dict, List, Optional

# ──────────────────────── Clue type constants ───────────────────────────

FACT = "FACT"
SAME = "SAME"
DIFFERENT = "DIFFERENT"
EXACTLY = "EXACTLY"
AT_LEAST = "AT_LEAST"
AT_MOST = "AT_MOST"
NEIGHBOR_COUNT = "NEIGHBOR_COUNT"
DIAGONAL = "DIAGONAL"

ALL_CLUE_TYPES = [FACT, SAME, DIFFERENT, EXACTLY, AT_LEAST, AT_MOST,
                  NEIGHBOR_COUNT, DIAGONAL]


# ──────────────────────── Validation ────────────────────────────────────

def validate_clue(clue: dict, all_names: List[str], board_size: int) -> bool:
    """Validate that a clue dict has correct structure and references."""
    ctype = clue.get("type")
    args = clue.get("args", {})

    if ctype not in ALL_CLUE_TYPES:
        return False

    if ctype == FACT:
        return (args.get("person") in all_names and
                args.get("status") in ("Criminal", "Innocent"))

    if ctype in (SAME, DIFFERENT):
        return (args.get("person1") in all_names and
                args.get("person2") in all_names and
                args["person1"] != args["person2"])

    if ctype in (EXACTLY, AT_LEAST, AT_MOST):
        region = args.get("region")
        count = args.get("count")
        if not isinstance(count, int) or count < 0:
            return False
        # Region validation is handled by Board.resolve_region
        return region is not None

    if ctype == NEIGHBOR_COUNT:
        return (args.get("cell") is not None and
                isinstance(args.get("count"), int) and
                args["count"] >= 0)

    if ctype == DIAGONAL:
        return (args.get("direction") in ("main", "anti") and
                isinstance(args.get("count"), int) and
                args["count"] >= 0)

    return False


# ──────────────────────── Semantic Evaluators ───────────────────────────

def evaluate_clue(clue: dict, assignment: Dict[str, bool],
                  board=None) -> bool:
    """Evaluate a clue against a complete assignment.
    
    Args:
        clue: structured clue dict
        assignment: mapping from character name -> True (Criminal) / False (Innocent)
        board: Board object (needed for region-based clues)
    
    Returns:
        True if the clue is satisfied by the assignment.
    
    This is a DIRECT semantic evaluator – it does not use CNF.
    """
    ctype = clue.get("type")
    args = clue.get("args", {})

    if ctype == FACT:
        person = args["person"]
        expected = args["status"] == "Criminal"
        return assignment.get(person) == expected

    if ctype == SAME:
        p1, p2 = args["person1"], args["person2"]
        return assignment.get(p1) == assignment.get(p2)

    if ctype == DIFFERENT:
        p1, p2 = args["person1"], args["person2"]
        return assignment.get(p1) != assignment.get(p2)

    if ctype in (EXACTLY, AT_LEAST, AT_MOST):
        if board is None:
            raise ValueError("Board required for region-based clue evaluation")
        region_cards = board.resolve_region(args["region"])
        criminal_count = sum(
            1 for card in region_cards if assignment.get(card.name, False)
        )
        k = args["count"]
        if ctype == EXACTLY:
            return criminal_count == k
        if ctype == AT_LEAST:
            return criminal_count >= k
        if ctype == AT_MOST:
            return criminal_count <= k

    if ctype == NEIGHBOR_COUNT:
        if board is None:
            raise ValueError("Board required for NEIGHBOR_COUNT clue")
        neighbors = board.get_neighbors(args["cell"])
        criminal_count = sum(
            1 for card in neighbors if assignment.get(card.name, False)
        )
        return criminal_count == args["count"]

    if ctype == DIAGONAL:
        if board is None:
            raise ValueError("Board required for DIAGONAL clue")
        diag_cards = board.get_diagonal(args["direction"])
        criminal_count = sum(
            1 for card in diag_cards if assignment.get(card.name, False)
        )
        return criminal_count == args["count"]

    raise ValueError(f"Unknown clue type: {ctype}")
