"""
Game Engine – owns the complete puzzle state (hidden solution + unrevealed clues).

Responsibilities:
  - Load puzzle from JSON
  - Process verdict submissions (calling LogicAgent for entailment check)
  - Flip cards and reveal clues on accepted verdicts
  - Track timer, move count
  - Provide public state to LogicAgent (never leaking hidden info)
  - Delegate Hint / Auto Solve to LogicAgent
  - Determine highlighted cells when a clue is selected
"""

from __future__ import annotations

import time
from typing import Dict, List, Optional

from game.board import Board
from game.card import Card
from logic.logic_agent import LogicAgent


class GameEngine:
    """Central game controller – owns hidden state, enforces game rules."""

    def __init__(self) -> None:
        self.board: Optional[Board] = None
        self.agent: Optional[LogicAgent] = None

        # Timing
        self._start_time: float = 0.0
        self._elapsed_before_pause: float = 0.0
        self._paused: bool = True

        # Counters
        self.move_count: int = 0
        self.is_finished: bool = False

        # Feedback message (shown briefly in GUI)
        self.last_feedback: Optional[dict] = None   # {"type": ..., "message": ...}

        # Auto-solve state
        self._auto_solving: bool = False

    # ──────────────────────── Loading ───────────────────────────

    def load_puzzle(self, json_path: str) -> None:
        """Load a puzzle and initialize the game."""
        self.board = Board()
        self.board.load(json_path)

        # Reveal initial cards
        for card in self.board.get_initially_revealed_cards():
            card.reveal()

        # Create logic agent with public info only
        self.agent = LogicAgent(
            character_names=self.board.get_all_names(),
            board=self.board,
        )
        self._sync_agent_knowledge()

        # Reset state
        self.move_count = 0
        self.is_finished = False
        self.last_feedback = None
        self._auto_solving = False

        # Start timer
        self._start_time = time.time()
        self._elapsed_before_pause = 0.0
        self._paused = False

    # ──────────────────────── Public State ──────────────────────

    def _sync_agent_knowledge(self) -> None:
        """Push current public knowledge to the logic agent."""
        if not self.board or not self.agent:
            return

        revealed_clues = []
        proven_verdicts: Dict[str, str] = {}

        for card in self.board.cards:
            if card.is_revealed:
                revealed_clues.append(card.clue)
                proven_verdicts[card.name] = card.proven_status

        self.agent.update_knowledge(revealed_clues, proven_verdicts)

    def get_public_state(self) -> dict:
        """Return only the public state (for display or Logic Agent)."""
        if not self.board:
            return {}

        return {
            "cards": [card.get_public_info() for card in self.board.cards],
            "board_name": self.board.name,
            "board_size": self.board.size,
            "revealed_count": self.board.revealed_count,
            "total_cards": self.board.total_cards,
            "is_finished": self.is_finished,
            "move_count": self.move_count,
            "elapsed_time": self.get_elapsed_time(),
        }

    # ──────────────────────── Verdict Submission ────────────────

    def submit_verdict(self, character_name: str, verdict: str) -> str:
        """Process a verdict submission.

        Args:
            character_name: name of the character
            verdict: "Criminal" or "Innocent"

        Returns:
            "ACCEPTED", "NOT_PROVABLE", or "CONTRADICTED"
        """
        if not self.board or not self.agent:
            return "NOT_PROVABLE"

        card = self.board.get_card_by_name(character_name)
        if card is None or card.is_revealed:
            return "NOT_PROVABLE"

        self.move_count += 1

        # Ask agent to classify this character
        classification = self.agent.classify(character_name)

        if classification == "UNKNOWN":
            self.last_feedback = {
                "type": "NOT_PROVABLE",
                "message": f"Chưa thể chứng minh trạng thái của {character_name}.",
            }
            return "NOT_PROVABLE"

        if classification == "INCONSISTENT":
            self.last_feedback = {
                "type": "CONTRADICTED",
                "message": "Knowledge base không nhất quán!",
            }
            return "CONTRADICTED"

        # classification is "Criminal" or "Innocent"
        if classification != verdict:
            # The opposite is forced
            self.last_feedback = {
                "type": "CONTRADICTED",
                "message": (f"{character_name} phải là {classification}, "
                            f"không phải {verdict}."),
            }
            return "CONTRADICTED"

        # Verdict is correct and provable → accept
        card.reveal()
        self._sync_agent_knowledge()

        self.last_feedback = {
            "type": "ACCEPTED",
            "message": f"{character_name} là {verdict}! Clue mới được mở.",
        }

        # Check win condition
        if self.board.all_revealed:
            self.is_finished = True
            self._paused = True

        return "ACCEPTED"

    # ──────────────────────── Hint ──────────────────────────────

    def request_hint(self) -> Optional[dict]:
        """Request a hint from the Logic Agent.

        Returns:
            {"character": name, "verdict": "Criminal"/"Innocent"} or None
        """
        if not self.agent:
            return None
        self._sync_agent_knowledge()
        return self.agent.hint()

    # ──────────────────────── Auto Solve ────────────────────────

    def auto_solve_step(self) -> Optional[dict]:
        """Perform one auto-solve step.

        Returns:
            {"character": ..., "verdict": ..., "step": DeductionStep} or None
        """
        if not self.agent or not self.board:
            return None

        self._sync_agent_knowledge()
        step = self.agent.auto_solve_step()

        if step is None:
            return None

        # Apply the verdict
        card = self.board.get_card_by_name(step.character)
        if card and not card.is_revealed:
            card.reveal()
            self._sync_agent_knowledge()
            self.move_count += 1

            if self.board.all_revealed:
                self.is_finished = True
                self._paused = True

        return {
            "character": step.character,
            "verdict": step.verdict,
            "step": step,
        }

    def auto_solve_all(self) -> List[dict]:
        """Run auto-solve to completion.

        Returns list of step dicts.
        """
        trace = []
        while not self.is_finished:
            result = self.auto_solve_step()
            if result is None:
                break
            trace.append(result)
        return trace

    # ──────────────────────── Highlight ─────────────────────────

    def get_highlighted_cells(self, clue_owner: str) -> List[str]:
        """Get cell IDs that are referenced by a character's clue."""
        if not self.board:
            return []

        card = self.board.get_card_by_name(clue_owner)
        if card is None or not card.is_revealed:
            return []

        def _extract_cells(clue_dict: dict) -> List[str]:
            ctype = clue_dict.get("type", "")
            args = clue_dict.get("args", {})
            cells = []

            if ctype in ("AND", "OR"):
                for sub_clue in args.get("clues", []):
                    cells.extend(_extract_cells(sub_clue))

            elif ctype in ("SAME", "DIFFERENT"):
                for key in ("person1", "person2"):
                    target = self.board.get_card_by_name(args.get(key, ""))
                    if target:
                        cells.append(target.cell_id)

            elif ctype == "FACT":
                target = self.board.get_card_by_name(args.get("person", ""))
                if target:
                    cells.append(target.cell_id)

            elif ctype in ("EXACTLY", "AT_LEAST", "AT_MOST"):
                region_cards = self.board.resolve_region(args.get("region"))
                cells.extend(c.cell_id for c in region_cards)

            elif ctype == "NEIGHBOR_COUNT":
                center_card = self.board.get_card_by_cell(args.get("cell", ""))
                if center_card:
                    cells.append(center_card.cell_id)
                neighbors = self.board.get_neighbors(args.get("cell", ""))
                cells.extend(c.cell_id for c in neighbors)

            elif ctype == "DIAGONAL":
                diag_cards = self.board.get_diagonal(args.get("direction", "main"))
                cells.extend(c.cell_id for c in diag_cards)

            elif ctype == "PATTERN_MATCH":
                r1 = self.board.resolve_region(args.get("region1"))
                r2 = self.board.resolve_region(args.get("region2"))
                cells.extend(c.cell_id for c in r1 + r2)

            return cells

        # Đảm bảo không bị trùng lặp ô khi highlight
        return list(set(_extract_cells(card.clue)))

    # ──────────────────────── Timer ─────────────────────────────

    def get_elapsed_time(self) -> float:
        """Return elapsed time in seconds."""
        if self._paused:
            return self._elapsed_before_pause
        return self._elapsed_before_pause + (time.time() - self._start_time)

    def pause_timer(self) -> None:
        if not self._paused:
            self._elapsed_before_pause += time.time() - self._start_time
            self._paused = True

    def resume_timer(self) -> None:
        if self._paused:
            self._start_time = time.time()
            self._paused = False

    # ──────────────────────── Restart ───────────────────────────

    def restart(self) -> None:
        """Reset the game to its initial state (same puzzle)."""
        if not self.board:
            return

        # Reset all cards
        for card in self.board.cards:
            card.is_revealed = False
            card.proven_status = None

        # Re-reveal initial cards
        for card in self.board.get_initially_revealed_cards():
            card.reveal()

        # Re-create agent
        self.agent = LogicAgent(
            character_names=self.board.get_all_names(),
            board=self.board,
        )
        self._sync_agent_knowledge()

        # Reset state
        self.move_count = 0
        self.is_finished = False
        self.last_feedback = None
        self._auto_solving = False
        self._start_time = time.time()
        self._elapsed_before_pause = 0.0
        self._paused = False

    # ──────────────────────── Stats ─────────────────────────────

    def get_stats(self) -> dict:
        """Return game and solver statistics."""
        agent_stats = self.agent.get_stats() if self.agent else {}
        encoder_stats = {}
        if self.agent:
            from logic.encoder import CNFEncoder
            enc = CNFEncoder(self.board.get_all_names(), self.board)
            revealed_clues = [c.clue for c in self.board.cards if c.is_revealed]
            proven = {c.name: c.proven_status for c in self.board.cards if c.is_revealed}
            enc.build_kb(revealed_clues, proven)
            encoder_stats = enc.get_stats()

        return {
            "move_count": self.move_count,
            "elapsed_time": self.get_elapsed_time(),
            "is_finished": self.is_finished,
            **agent_stats,
            **encoder_stats,
        }
