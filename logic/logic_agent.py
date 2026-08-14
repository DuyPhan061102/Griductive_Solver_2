from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from logic.cnf import CNFFormula
from logic.dpll import DPLLSolver, DPLLStats
from logic.encoder import CNFEncoder


class DeductionStep:
    def __init__(self) -> None:
        self.step_number: int = 0
        self.character: str = ""
        self.verdict: str = ""               
        self.result: str = ""                
        self.active_clues: List[str] = []    
        self.sat_queries: int = 0           
        self.newly_revealed_clue: Optional[dict] = None
        self.stats: Optional[DPLLStats] = None

    def __repr__(self) -> str:
        return (f"Step {self.step_number}: {self.character} → "
                f"{self.verdict} ({self.result})")


class LogicAgent:
    def __init__(self, character_names: List[str], board=None) -> None:
        self.character_names = character_names
        self.board = board
        self.solver = DPLLSolver()

        self.revealed_clues: List[dict] = []
        self.proven_verdicts: Dict[str, str] = {} 

        self.total_sat_calls: int = 0
        self.total_stats = DPLLStats()
        self.deduction_trace: List[DeductionStep] = []

    def update_knowledge(self, revealed_clues: List[dict],
                         proven_verdicts: Dict[str, str]) -> None:
        self.revealed_clues = list(revealed_clues)
        self.proven_verdicts = dict(proven_verdicts)

    def _build_kb(self) -> Tuple[CNFEncoder, CNFFormula]:
        encoder = CNFEncoder(self.character_names, self.board)
        kb = encoder.build_kb(self.revealed_clues, self.proven_verdicts)
        return encoder, kb

    def classify(self, character_name: str) -> str:
        encoder, kb = self._build_kb()
        var = encoder.char_to_var[character_name]

        kb_neg = kb.copy()
        kb_neg.add_unit(-var)
        sat_neg, _ = self.solver.solve(kb_neg)
        self.total_sat_calls += 1

        kb_pos = kb.copy()
        kb_pos.add_unit(var)
        sat_pos, _ = self.solver.solve(kb_pos)
        self.total_sat_calls += 1

        if not sat_neg and not sat_pos:
            return "INCONSISTENT"
        if not sat_neg:
            return "Criminal"    
        if not sat_pos:
            return "Innocent"    
        return "UNKNOWN"

    def classify_all(self) -> Dict[str, str]:
        results = {}
        for name in self.character_names:
            if name in self.proven_verdicts:
                results[name] = self.proven_verdicts[name]
            else:
                results[name] = self.classify(name)
        return results

    def hint(self) -> Optional[Dict]:
        for name in self.character_names:
            if name in self.proven_verdicts:
                continue
            result = self.classify(name)
            if result in ("Criminal", "Innocent"):
                return {"character": name, "verdict": result}
        return None

    def auto_solve_step(self) -> Optional[DeductionStep]:
        sat_calls_before = self.total_sat_calls

        for name in self.character_names:
            if name in self.proven_verdicts:
                continue
            result = self.classify(name)
            if result in ("Criminal", "Innocent"):
                step = DeductionStep()
                step.step_number = len(self.deduction_trace) + 1
                step.character = name
                step.verdict = result
                step.result = "ACCEPTED"
                step.sat_queries = self.total_sat_calls - sat_calls_before
                step.active_clues = [
                    f"{c.get('type', '?')}({c.get('args', {})})"
                    for c in self.revealed_clues
                ]
                step.stats = DPLLStats()
                step.stats.decisions = self.solver.stats.decisions
                step.stats.propagations = self.solver.stats.propagations
                step.stats.backtracks = self.solver.stats.backtracks
                step.stats.runtime_ms = self.solver.stats.runtime_ms

                self.deduction_trace.append(step)
                return step

        return None

    def check_uniqueness(self, all_clues: List[dict]) -> bool:
        encoder = CNFEncoder(self.character_names, self.board)
        for clue in all_clues:
            encoder.encode_clue(clue)

        formula = encoder.formula

        sat1, assignment1 = self.solver.solve(formula)
        if not sat1:
            return False  

        blocking_clause = []
        for name in self.character_names:
            var = encoder.char_to_var[name]
            if assignment1[var]:
                blocking_clause.append(-var)
            else:
                blocking_clause.append(var)

        formula2 = formula.copy()
        formula2.add_clause(blocking_clause)

        sat2, _ = self.solver.solve(formula2)
        return not sat2  

    def get_stats(self) -> dict:
        return {
            "total_sat_calls": self.total_sat_calls,
            "deduction_steps": len(self.deduction_trace),
            "total_decisions": sum(
                s.stats.decisions for s in self.deduction_trace if s.stats
            ),
            "total_propagations": sum(
                s.stats.propagations for s in self.deduction_trace if s.stats
            ),
            "total_backtracks": sum(
                s.stats.backtracks for s in self.deduction_trace if s.stats
            ),
        }
