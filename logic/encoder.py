"""
CNF Encoder – converts structured clues into CNF formulas.

Responsibilities:
  - Create deterministic mapping: character name → propositional variable Ci
  - Convert all 8 clue types to CNF clauses
  - Add known verdicts as unit clauses
  - Build knowledge base KBt at each deduction step

TODO (Người 2): Implement full CNF encoding for all clue types.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from logic.cnf import CNFFormula


class CNFEncoder:
    """Encodes clues and verdicts into a CNF formula."""

    def __init__(self, character_names: List[str], board=None) -> None:
        """Initialize encoder with character-to-variable mapping.
        
        Args:
            character_names: list of all character names (deterministic order)
            board: Board object for resolving regions
        """
        self.board = board
        self.formula = CNFFormula()
        self.char_to_var: Dict[str, int] = {}

        # Create primary variables: Ci = True means character i is Criminal
        for name in character_names:
            var = self.formula.new_variable(name)
            self.char_to_var[name] = var

    def encode_clue(self, clue: dict) -> None:
        """Convert a structured clue to CNF clauses and add to formula.
        
        TODO (Người 2): Implement CNF encoding for each clue type:
          - FACT:           unit clause
          - SAME:           Ci ↔ Cj  →  (¬Ci ∨ Cj) ∧ (Ci ∨ ¬Cj)
          - DIFFERENT:      Ci ⊕ Cj  →  (Ci ∨ Cj) ∧ (¬Ci ∨ ¬Cj)
          - EXACTLY(k, R):  cardinality constraint = k
          - AT_LEAST(k, R): cardinality constraint >= k
          - AT_MOST(k, R):  cardinality constraint <= k
          - NEIGHBOR_COUNT: like EXACTLY but on neighbor region
          - DIAGONAL:       like EXACTLY but on diagonal region
        """
        ctype = clue.get("type")
        args = clue.get("args", {})

        if ctype == "FACT":
            var = self.char_to_var[args["person"]]
            lit = var if args["status"] == "Criminal" else -var
            self.formula.add_unit(lit)

        elif ctype == "SAME":
            vi = self.char_to_var[args["person1"]]
            vj = self.char_to_var[args["person2"]]
            # Ci ↔ Cj  ≡  (¬Ci ∨ Cj) ∧ (Ci ∨ ¬Cj)
            self.formula.add_clause([-vi, vj])
            self.formula.add_clause([vi, -vj])

        elif ctype == "DIFFERENT":
            vi = self.char_to_var[args["person1"]]
            vj = self.char_to_var[args["person2"]]
            # Ci ⊕ Cj  ≡  (Ci ∨ Cj) ∧ (¬Ci ∨ ¬Cj)
            self.formula.add_clause([vi, vj])
            self.formula.add_clause([-vi, -vj])

        elif ctype in ("EXACTLY", "AT_LEAST", "AT_MOST",
                        "NEIGHBOR_COUNT", "DIAGONAL"):
            self._encode_counting_clue(ctype, args)

        else:
            raise ValueError(f"Unknown clue type: {ctype}")

    def _encode_counting_clue(self, ctype: str, args: dict) -> None:
        """Encode counting constraints using combinatorial encoding.
        
        For small regions (≤25 cells), we use direct combinatorial encoding:
          EXACTLY(k, R):  AT_MOST(k, R) ∧ AT_LEAST(k, R)
          AT_MOST(k, R):  for every subset S of R with |S| = k+1, add ¬(all of S)
          AT_LEAST(k, R): for every subset S of R with |S| = |R|-k+1, add (at least one of S)
        """
        # Determine region and count
        if ctype == "NEIGHBOR_COUNT":
            region_cards = self.board.get_neighbors(args["cell"])
            k = args["count"]
        elif ctype == "DIAGONAL":
            region_cards = self.board.get_diagonal(args["direction"])
            k = args["count"]
        else:
            region_cards = self.board.resolve_region(args["region"])
            k = args["count"]

        vars_in_region = [self.char_to_var[c.name] for c in region_cards]
        n = len(vars_in_region)

        if ctype in ("EXACTLY", "NEIGHBOR_COUNT", "DIAGONAL"):
            # EXACTLY(k) = AT_MOST(k) ∧ AT_LEAST(k)
            self._encode_at_most(vars_in_region, k)
            self._encode_at_least(vars_in_region, k)
        elif ctype == "AT_MOST":
            self._encode_at_most(vars_in_region, k)
        elif ctype == "AT_LEAST":
            self._encode_at_least(vars_in_region, k)

    def _encode_at_most(self, variables: List[int], k: int) -> None:
        """Encode: at most k of the variables are True.
        
        For every subset of size k+1, at least one must be False.
        """
        from itertools import combinations
        n = len(variables)
        if k >= n:
            return  # trivially true
        for subset in combinations(variables, k + 1):
            # At least one in subset must be False → clause of negations
            self.formula.add_clause([-v for v in subset])

    def _encode_at_least(self, variables: List[int], k: int) -> None:
        """Encode: at least k of the variables are True.
        
        For every subset of size n-k+1, at least one must be True.
        """
        from itertools import combinations
        n = len(variables)
        if k <= 0:
            return  # trivially true
        for subset in combinations(variables, n - k + 1):
            # At least one in subset must be True → clause of positives
            self.formula.add_clause(list(subset))

    def add_verdict(self, character_name: str, is_criminal: bool) -> None:
        """Add a known verdict as a unit clause."""
        var = self.char_to_var[character_name]
        self.formula.add_unit(var if is_criminal else -var)

    def build_kb(self, revealed_clues: List[dict],
                 proven_verdicts: Dict[str, str]) -> CNFFormula:
        """Build knowledge base at current deduction step.
        
        Args:
            revealed_clues: list of revealed clue dicts
            proven_verdicts: {character_name: "Criminal" or "Innocent"}
        
        Returns:
            CNF formula representing KBt
        """
        # Reset formula but keep variable mapping
        old_vars = self.formula.var_names.copy()
        old_names = self.formula.name_to_var.copy()
        old_num = self.formula.num_vars

        self.formula = CNFFormula()
        self.formula.var_names = old_vars
        self.formula.name_to_var = old_names
        self.formula.num_vars = old_num

        # Encode all revealed clues
        for clue in revealed_clues:
            self.encode_clue(clue)

        # Add proven verdicts as unit clauses
        for name, status in proven_verdicts.items():
            self.add_verdict(name, status == "Criminal")

        return self.formula

    def get_stats(self) -> dict:
        """Return encoding statistics."""
        return {
            "primary_vars": len(self.char_to_var),
            "auxiliary_vars": self.formula.num_auxiliary_vars,
            "total_vars": self.formula.num_vars,
            "clauses": self.formula.num_clauses,
        }
