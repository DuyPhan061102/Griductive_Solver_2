"""
DPLL SAT Solver – Davis-Putnam-Logemann-Loveland procedure.

Implements:
  1. Unit propagation
  2. Conflict detection
  3. Deterministic variable selection
  4. Recursive branching and backtracking
  5. Returns SAT (with assignment) or UNSAT
  6. Records decisions, propagations, backtracks, and runtime

TODO (Người 2): Optionally add pure-literal elimination and
                advanced branching heuristics.
"""

from __future__ import annotations

import time
from typing import Dict, List, Optional, Set, Tuple

from logic.cnf import CNFFormula


class DPLLStats:
    """Statistics recorded during DPLL execution."""

    def __init__(self) -> None:
        self.decisions: int = 0
        self.propagations: int = 0
        self.backtracks: int = 0
        self.runtime_ms: float = 0.0

    def __repr__(self) -> str:
        return (f"DPLLStats(decisions={self.decisions}, "
                f"propagations={self.propagations}, "
                f"backtracks={self.backtracks}, "
                f"runtime={self.runtime_ms:.2f}ms)")


class DPLLSolver:
    """DPLL SAT solver with unit propagation and backtracking."""

    def __init__(self) -> None:
        self.stats = DPLLStats()

    def solve(self, formula: CNFFormula,
              assumptions: Optional[List[int]] = None) -> Tuple[bool, Optional[Dict[int, bool]]]:
        """Solve a CNF formula.
        
        Args:
            formula: CNF formula to solve
            assumptions: optional list of assumed literals (added as unit clauses)
        
        Returns:
            (is_satisfiable, assignment)
            - assignment maps variable_id -> True/False (only if SAT)
        """
        self.stats = DPLLStats()
        start_time = time.perf_counter()

        # Copy clauses so we don't modify the original
        clauses = [clause[:] for clause in formula.clauses]

        # Add assumptions as unit clauses
        if assumptions:
            for lit in assumptions:
                clauses.append([lit])

        # Initial assignment
        assignment: Dict[int, bool] = {}

        result = self._dpll(clauses, assignment, formula.num_vars)

        elapsed = (time.perf_counter() - start_time) * 1000
        self.stats.runtime_ms = elapsed

        if result:
            # Fill in any unassigned variables (don't-care) as False
            for v in range(1, formula.num_vars + 1):
                if v not in assignment:
                    assignment[v] = False
            return True, assignment
        else:
            return False, None

    def _dpll(self, clauses: List[List[int]],
              assignment: Dict[int, bool],
              num_vars: int) -> bool:
        """Core DPLL recursive procedure."""

        # ── Unit Propagation ──
        changed = True
        while changed:
            changed = False
            for clause in clauses:
                unresolved = []
                satisfied = False
                for lit in clause:
                    var = abs(lit)
                    if var in assignment:
                        val = assignment[var]
                        if (lit > 0 and val) or (lit < 0 and not val):
                            satisfied = True
                            break
                    else:
                        unresolved.append(lit)

                if satisfied:
                    continue

                if len(unresolved) == 0:
                    # Conflict: empty clause
                    return False
                elif len(unresolved) == 1:
                    # Unit clause: propagate
                    lit = unresolved[0]
                    var = abs(lit)
                    val = lit > 0
                    assignment[var] = val
                    self.stats.propagations += 1
                    changed = True
                    break  # restart scan after propagation

        # ── Conflict Detection ──
        for clause in clauses:
            all_false = True
            has_unresolved = False
            for lit in clause:
                var = abs(lit)
                if var not in assignment:
                    has_unresolved = True
                    all_false = False
                    break
                val = assignment[var]
                if (lit > 0 and val) or (lit < 0 and not val):
                    all_false = False
                    break
            if all_false and not has_unresolved:
                return False

        # ── Check if all clauses are satisfied ──
        all_satisfied = True
        for clause in clauses:
            satisfied = False
            for lit in clause:
                var = abs(lit)
                if var in assignment:
                    val = assignment[var]
                    if (lit > 0 and val) or (lit < 0 and not val):
                        satisfied = True
                        break
            if not satisfied:
                # Check if there are unresolved literals
                has_unresolved = any(abs(lit) not in assignment for lit in clause)
                if not has_unresolved:
                    return False  # unsatisfied and no unresolved
                all_satisfied = False

        if all_satisfied:
            return True

        # ── Variable Selection (deterministic: smallest unassigned) ──
        branch_var = None
        for v in range(1, num_vars + 1):
            if v not in assignment:
                branch_var = v
                break

        if branch_var is None:
            return True  # all assigned and no conflicts

        # ── Branching ──
        self.stats.decisions += 1

        # Try True first
        assignment_copy = dict(assignment)
        assignment_copy[branch_var] = True
        if self._dpll(clauses, assignment_copy, num_vars):
            assignment.update(assignment_copy)
            return True

        self.stats.backtracks += 1

        # Try False
        assignment_copy2 = dict(assignment)
        assignment_copy2[branch_var] = False
        if self._dpll(clauses, assignment_copy2, num_vars):
            assignment.update(assignment_copy2)
            return True

        self.stats.backtracks += 1
        return False
