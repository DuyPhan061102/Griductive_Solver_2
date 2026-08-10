"""
CNF Encoder – converts structured clues into CNF formulas with optimized cardinality encoding.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple
from itertools import combinations
from logic.cnf import CNFFormula


class CNFEncoder:
    """Encodes clues and verdicts into a CNF formula."""

    def __init__(self, character_names: List[str], board=None) -> None:
        """Initialize encoder with character-to-variable mapping."""
        self.board = board
        self.character_names = character_names
        self.formula = CNFFormula()
        self.char_to_var: Dict[str, int] = {}
        self.proven_verdicts: Dict[str, str] = {}

        # Create primary variables: Ci = True means character i is Criminal
        for name in character_names:
            var = self.formula.new_variable(name)
            self.char_to_var[name] = var

    # ────────────────────── Helpers & Wrappers ──────────────────────

    def get_var(self, person_name: str) -> int:
        """Lấy ID biến mệnh đề (số nguyên > 0) tương ứng với tên nhân vật."""
        if hasattr(self, "char_to_var") and person_name in self.char_to_var:
            return self.char_to_var[person_name]
        if hasattr(self, "formula") and person_name in self.formula.name_to_var:
            return self.formula.name_to_var[person_name]
        if hasattr(self, "character_names") and person_name in self.character_names:
            return self.character_names.index(person_name) + 1

        raise KeyError(f"Không tìm thấy biến mệnh đề cho nhân vật: {person_name}")

    def add_clause(self, clause: List[int]) -> None:
        """Thêm 1 clause vào công thức CNF."""
        self.formula.add_clause(clause)

    def _filter_known_vars(self, variables: List[int], k: int) -> Tuple[List[int], int]:
        """Lọc bỏ các biến đã biết trạng thái để tránh bùng nổ tổ hợp."""
        if not hasattr(self, "proven_verdicts") or not self.proven_verdicts:
            return variables, k

        unsolved_vars = []
        eff_k = k
        for v in variables:
            name = self.formula.var_names.get(v, "")
            if name in self.proven_verdicts:
                if self.proven_verdicts[name] == "Criminal":
                    eff_k -= 1  # Đã biết là Criminal -> giảm số lượng cần đếm
            else:
                unsolved_vars.append(v)
        return unsolved_vars, eff_k

    def add_cardinality_exactly(self, variables: List[int], k: int) -> None:
        """Ràng buộc EXACTLY k biến trong danh sách mang giá trị True."""
        unsolved_vars, eff_k = self._filter_known_vars(variables, k)
        if eff_k < 0 or eff_k > len(unsolved_vars):
            self.add_clause([])  # Mâu thuẫn logic
            return
        self._encode_at_most(unsolved_vars, eff_k)
        self._encode_at_least(unsolved_vars, eff_k)

    def add_cardinality_at_least(self, variables: List[int], k: int) -> None:
        """Ràng buộc AT LEAST k biến trong danh sách mang giá trị True."""
        unsolved_vars, eff_k = self._filter_known_vars(variables, k)
        if eff_k <= 0:
            return
        if eff_k > len(unsolved_vars):
            self.add_clause([])
            return
        self._encode_at_least(unsolved_vars, eff_k)

    def add_cardinality_at_most(self, variables: List[int], k: int) -> None:
        """Ràng buộc AT MOST k biến trong danh sách mang giá trị True."""
        unsolved_vars, eff_k = self._filter_known_vars(variables, k)
        if eff_k < 0:
            self.add_clause([])
            return
        if eff_k >= len(unsolved_vars):
            return
        self._encode_at_most(unsolved_vars, eff_k)

    # ────────────────────── Clue Encoding ──────────────────────

    def encode_clue(self, clue: dict) -> None:
        """Convert a structured clue dict into CNF clauses and add to KB."""
        if not clue:
            return

        ctype = clue.get("type", "")
        args = clue.get("args", {})

        # ── 1. Clue phức hợp AND ──
        if ctype == "AND":
            for sub_clue in args.get("clues", []):
                self.encode_clue(sub_clue)
            return

        # ── 2. Clue phức hợp OR ──
        elif ctype == "OR":
            self._encode_or(args.get("clues", []))
            return

        # ── 3. Clue FACT ──
        elif ctype == "FACT":
            person = args["person"]
            status = args["status"]
            var = self.get_var(person)
            if status == "Criminal":
                self.add_clause([var])
            else:
                self.add_clause([-var])
            return

        # ── 4. Clue SAME ──
        elif ctype == "SAME":
            v1 = self.get_var(args["person1"])
            v2 = self.get_var(args["person2"])
            self.add_clause([-v1, v2])
            self.add_clause([v1, -v2])
            return

        # ── 5. Clue DIFFERENT ──
        elif ctype == "DIFFERENT":
            v1 = self.get_var(args["person1"])
            v2 = self.get_var(args["person2"])
            self.add_clause([v1, v2])
            self.add_clause([-v1, -v2])
            return

        # ── 6. Clue đếm EXACTLY / AT_LEAST / AT_MOST ──
        elif ctype in ("EXACTLY", "AT_LEAST", "AT_MOST"):
            region = args["region"]
            count = args["count"]
            region_cards = self.board.resolve_region(region) if self.board else []
            vars_list = [self.get_var(c.name) for c in region_cards]

            if ctype == "EXACTLY":
                self.add_cardinality_exactly(vars_list, count)
            elif ctype == "AT_LEAST":
                self.add_cardinality_at_least(vars_list, count)
            elif ctype == "AT_MOST":
                self.add_cardinality_at_most(vars_list, count)
            return

        # ── 7. Extension: NEIGHBOR_COUNT ──
        elif ctype == "NEIGHBOR_COUNT":
            cell_id = args["cell"]
            count = args["count"]
            neighbors = self.board.get_neighbors(cell_id) if self.board else []
            vars_list = [self.get_var(c.name) for c in neighbors]
            self.add_cardinality_exactly(vars_list, count)
            return

        # ── 8. Extension: DIAGONAL ──
        elif ctype == "DIAGONAL":
            direction = args.get("direction", "main")
            count = args["count"]
            diag_cards = self.board.get_diagonal(direction) if self.board else []
            vars_list = [self.get_var(c.name) for c in diag_cards]
            self.add_cardinality_exactly(vars_list, count)
            return

        # ── 9. Extension: GLOBAL_TOTAL ──
        elif ctype == "GLOBAL_TOTAL":
            count = args["count"]
            all_vars = [self.get_var(name) for name in self.character_names]
            self.add_cardinality_exactly(all_vars, count)
            return

        # ── 10. Extension: NO_ADJACENT ──
        elif ctype == "NO_ADJACENT":
            if self.board:
                for card in self.board.cards:
                    v1 = self.get_var(card.name)
                    r, c = card.grid_row, card.grid_col
                    for dr, dc in [(0, 1), (1, 0)]:
                        nbr = self.board.get_card_at(r + dr, c + dc)
                        if nbr:
                            v2 = self.get_var(nbr.name)
                            self.add_clause([-v1, -v2])
            return

        # ── 11. Extension: PATTERN_MATCH ──
        elif ctype == "PATTERN_MATCH":
            if self.board:
                r1_cards = self.board.resolve_region(args["region1"])
                r2_cards = self.board.resolve_region(args["region2"])
                for c1, c2 in zip(r1_cards, r2_cards):
                    v1 = self.get_var(c1.name)
                    v2 = self.get_var(c2.name)
                    self.add_clause([-v1, v2])
                    self.add_clause([v1, -v2])
            return

    def _encode_or(self, sub_clues: list) -> None:
        """Xử lý phân phối mệnh đề cho phép OR giữa các clue con."""
        import itertools

        def _extract_lits(sub):
            stype = sub.get("type", "")
            sargs = sub.get("args", {})
            if stype == "FACT":
                v = self.get_var(sargs["person"])
                return [[v if sargs["status"] == "Criminal" else -v]]
            elif stype == "AND":
                res = []
                for child in sargs.get("clues", []):
                    res.extend(_extract_lits(child))
                return res
            elif stype == "EXACTLY" and sargs.get("count") == 0:
                region_cards = self.board.resolve_region(sargs["region"]) if self.board else []
                return [[-self.get_var(c.name)] for c in region_cards]
            elif stype == "DIAGONAL":
                diag_cards = self.board.get_diagonal(sargs.get("direction", "main")) if self.board else []
                if sargs.get("count") == len(diag_cards):
                    return [[self.get_var(c.name)] for c in diag_cards]
                elif sargs.get("count") == 0:
                    return [[-self.get_var(c.name)] for c in diag_cards]
            return []

        clause_options = [_extract_lits(s) for s in sub_clues]
        clause_options = [c for c in clause_options if c]

        if not clause_options:
            return

        if all(len(c) == 1 and len(c[0]) == 1 for c in clause_options):
            or_clause = [c[0][0] for c in clause_options]
            self.add_clause(or_clause)
        else:
            flat_options = []
            for opt in clause_options:
                flat = [item for sublist in opt for item in sublist]
                if flat:
                    flat_options.append(flat)
            if flat_options:
                for combo in itertools.product(*flat_options):
                    self.add_clause(list(combo))

    # ────────────────────── Cardinality Encoding Helpers ──────────────────────

    def _encode_at_most(self, variables: List[int], k: int) -> None:
        """Encode: at most k of the variables are True."""
        n = len(variables)
        if k >= n:
            return
        for subset in combinations(variables, k + 1):
            self.add_clause([-v for v in subset])

    def _encode_at_least(self, variables: List[int], k: int) -> None:
        """Encode: at least k of the variables are True."""
        n = len(variables)
        if k <= 0:
            return
        for subset in combinations(variables, n - k + 1):
            self.add_clause(list(subset))

    def add_verdict(self, character_name: str, is_criminal: bool) -> None:
        """Add a known verdict as a unit clause."""
        var = self.get_var(character_name)
        self.formula.add_unit(var if is_criminal else -var)

    def build_kb(self, revealed_clues: List[dict],
                 proven_verdicts: Dict[str, str]) -> CNFFormula:
        """Build knowledge base at current deduction step."""
        self.proven_verdicts = proven_verdicts  # [LƯU LẠI CÁC Ô ĐÃ GIẢI]

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