"""
CNF data structures for propositional logic.

A CNF formula is a conjunction (AND) of clauses.
Each clause is a disjunction (OR) of literals.
A literal is a positive or negative integer (variable index).
  - Positive int  → variable is True
  - Negative int  → variable is False

Example: [[1, -2], [2, 3]] represents (x1 ∨ ¬x2) ∧ (x2 ∨ x3)
"""

from __future__ import annotations

from typing import Dict, List, Optional, Set


class CNFFormula:
    """A CNF formula represented as a list of clauses."""

    def __init__(self) -> None:
        self.clauses: List[List[int]] = []
        self.num_vars: int = 0
        self.var_names: Dict[int, str] = {}    # var_id -> human-readable name
        self.name_to_var: Dict[str, int] = {}  # human-readable name -> var_id

    def add_clause(self, clause: List[int]) -> None:
        """Add a clause (list of literals) to the formula."""
        self.clauses.append(clause)
        for lit in clause:
            var = abs(lit)
            if var > self.num_vars:
                self.num_vars = var

    def add_unit(self, literal: int) -> None:
        """Add a unit clause (single literal)."""
        self.add_clause([literal])

    def new_variable(self, name: str = "") -> int:
        """Create and return a new variable ID."""
        self.num_vars += 1
        var_id = self.num_vars
        if name:
            self.var_names[var_id] = name
            self.name_to_var[name] = var_id
        return var_id

    def get_variable(self, name: str) -> Optional[int]:
        """Get variable ID by name, or None if not found."""
        return self.name_to_var.get(name)

    @property
    def num_clauses(self) -> int:
        return len(self.clauses)

    @property
    def num_primary_vars(self) -> int:
        """Count of primary (character) variables only."""
        return sum(1 for name in self.var_names.values()
                   if not name.startswith("_aux"))

    @property
    def num_auxiliary_vars(self) -> int:
        """Count of auxiliary variables introduced by encodings."""
        return self.num_vars - self.num_primary_vars

    def copy(self) -> CNFFormula:
        """Create a deep copy of this formula."""
        new_formula = CNFFormula()
        new_formula.clauses = [clause[:] for clause in self.clauses]
        new_formula.num_vars = self.num_vars
        new_formula.var_names = dict(self.var_names)
        new_formula.name_to_var = dict(self.name_to_var)
        return new_formula

    def __repr__(self) -> str:
        return (f"CNFFormula(vars={self.num_vars}, "
                f"clauses={self.num_clauses})")
