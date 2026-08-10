"""
Board model – an N×N grid of Card objects.

Handles:
  - Loading puzzle data from JSON
  - Grid queries: row, column, neighbors, region lookup
  - Providing the initial face-up cards
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List, Optional

from game.card import Card


class Board:
    """N×N grid of Card objects loaded from a puzzle JSON file."""

    def __init__(self) -> None:
        self.name: str = ""
        self.size: int = 0                    # N (3, 4, or 5)
        self.columns: List[str] = []          # ["A", "B", "C", ...]
        self.cards: List[Card] = []           # flat list, row-major order
        self.initially_revealed: List[str] = []  # character names revealed at start
        self._cell_map: dict[str, Card] = {}  # cell_id -> Card
        self._name_map: dict[str, Card] = {}  # character name -> Card

    # ────────────────────── loading ──────────────────────────

    def load(self, json_path: str) -> None:
        """Load a puzzle from a JSON file."""
        path = Path(json_path)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.name = data.get("name", path.stem)
        self.size = data["size"]
        self.columns = data.get("columns", [chr(ord("A") + i) for i in range(self.size)])
        
        # Hỗ trợ cả 2 kiểu đặt tên key trong JSON
        self.initially_revealed = data.get("initially_revealed") or data.get("initial_revealed", [])

        self.cards = []
        self._cell_map = {}
        self._name_map = {}

        for card_data in data["cards"]:
            card = Card(
                cell_id=card_data["cell"],
                name=card_data["name"],
                occupation=card_data["occupation"],
                true_status=card_data["status"],
                clue=card_data["clue"],
            )
            self.cards.append(card)
            self._cell_map[card.cell_id] = card
            self._name_map[card.name] = card

        # Sort cards in row-major order (A1, B1, C1, A2, B2, ...)
        self.cards.sort(key=lambda c: (c.row_number, c.grid_col))

    # ────────────────────── accessors ────────────────────────

    def get_card_by_cell(self, cell_id: str) -> Optional[Card]:
        """Get card at a specific cell (e.g. 'A1')."""
        return self._cell_map.get(cell_id)

    def get_card_by_name(self, name: str) -> Optional[Card]:
        """Get card by character name (e.g. 'Alice')."""
        return self._name_map.get(name)

    def get_card_at(self, row: int, col: int) -> Optional[Card]:
        """Get card at grid position (0-based row, 0-based col)."""
        if 0 <= row < self.size and 0 <= col < self.size:
            cell_id = f"{chr(ord('A') + col)}{row + 1}"
            return self._cell_map.get(cell_id)
        return None

    def get_row(self, row_number: int) -> List[Card]:
        """Get all cards in a row (1-based row number)."""
        return [c for c in self.cards if c.row_number == row_number]

    def get_column(self, col_letter: str) -> List[Card]:
        """Get all cards in a column (e.g. 'A')."""
        return [c for c in self.cards if c.col_letter == col_letter]

    def get_neighbors(self, cell_id: str) -> List[Card]:
        """Get all neighboring cards (8-directional, excluding self)."""
        card = self._cell_map.get(cell_id)
        if card is None:
            return []
        r, c = card.grid_row, card.grid_col
        neighbors = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                neighbor = self.get_card_at(nr, nc)
                if neighbor is not None:
                    neighbors.append(neighbor)
        return neighbors

    def get_diagonal(self, direction: str) -> List[Card]:
        """Get all cards on a diagonal.
        
        direction: 'main' (top-left to bottom-right) or 'anti' (top-right to bottom-left).
        Only works for square grids.
        """
        result = []
        for i in range(self.size):
            if direction == "main":
                card = self.get_card_at(i, i)
            else:  # anti
                card = self.get_card_at(i, self.size - 1 - i)
            if card is not None:
                result.append(card)
        return result

    def resolve_region(self, region) -> List[Card]:
        """Convert a region specifier to a list of Card objects."""
        if isinstance(region, list):
            # Explicit list of character names
            return [self._name_map[name] for name in region if name in self._name_map]

        if isinstance(region, str):
            # Xử lý vùng 4 góc
            if region == "corners":
                corners = [
                    self.get_card_at(0, 0),
                    self.get_card_at(0, self.size - 1),
                    self.get_card_at(self.size - 1, 0),
                    self.get_card_at(self.size - 1, self.size - 1),
                ]
                return [c for c in corners if c is not None]

            # Xử lý cả 2 đường chéo
            if region == "all_diagonals":
                main_d = self.get_diagonal("main")
                anti_d = self.get_diagonal("anti")
                seen = set()
                res = []
                for c in main_d + anti_d:
                    if c.cell_id not in seen:
                        seen.add(c.cell_id)
                        res.append(c)
                return res

            if region.startswith("row_"):
                return self.get_row(int(region[4:]))
            if region.startswith("col_"):
                return self.get_column(region[4:])
            if region.startswith("neighbors_"):
                return self.get_neighbors(region[10:])
            if region.startswith("diagonal_"):
                return self.get_diagonal(region[9:])

        return []

    def get_initially_revealed_cards(self) -> List[Card]:
        """Return cards that start face-up."""
        return [
            self._name_map[name]
            for name in self.initially_revealed
            if name in self._name_map
        ]

    def get_all_names(self) -> List[str]:
        """Return all character names in row-major order."""
        return [c.name for c in self.cards]

    def get_unsolved_cards(self) -> List[Card]:
        """Return cards that have not been solved yet."""
        return [c for c in self.cards if not c.is_solved]

    @property
    def total_cards(self) -> int:
        return len(self.cards)

    @property
    def revealed_count(self) -> int:
        return sum(1 for c in self.cards if c.is_revealed)

    @property
    def all_revealed(self) -> bool:
        return all(c.is_revealed for c in self.cards)

    def __repr__(self) -> str:
        return f"Board({self.name}, {self.size}x{self.size}, {self.revealed_count}/{self.total_cards} revealed)"
