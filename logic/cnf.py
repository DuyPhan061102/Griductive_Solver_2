from __future__ import annotations

from typing import Dict, List, Optional, Set


class CNFFormula:
    def __init__(self) -> None:
        self.clauses: List[List[int]] = []
        self.num_vars: int = 0
        self.var_names: Dict[int, str] = {}
        self.name_to_var: Dict[str, int] = {}

    def add_clause(self, clause: List[int]) -> None:
        self.clauses.append(clause)
        for lit in clause:
            var = abs(lit)
            if var > self.num_vars:
                self.num_vars = var

    def add_unit(self, literal: int) -> None:
        self.add_clause([literal])

    def new_variable(self, name: str = "") -> int:
        self.num_vars += 1
        var_id = self.num_vars
        if name:
            self.var_names[var_id] = name
            self.name_to_var[name] = var_id
        return var_id

    def get_variable(self, name: str) -> Optional[int]:
        return self.name_to_var.get(name)

    @property
    def num_clauses(self) -> int:
        return len(self.clauses)

    @property
    def num_primary_vars(self) -> int:
        return sum(1 for name in self.var_names.values()
                   if not name.startswith("_aux"))

    @property
    def num_auxiliary_vars(self) -> int:
        return self.num_vars - self.num_primary_vars

    def copy(self) -> CNFFormula:
        new_formula = CNFFormula()
        new_formula.clauses = [clause[:] for clause in self.clauses]
        new_formula.num_vars = self.num_vars
        new_formula.var_names = dict(self.var_names)
        new_formula.name_to_var = dict(self.name_to_var)
        return new_formula

    def __repr__(self) -> str:
        return (f"CNFFormula(vars={self.num_vars}, "
                f"clauses={self.num_clauses})")
