"""
Card model – represents a single cell on the Griductive board.

Each card holds:
  - identity   (cell id, character name, occupation)
  - hidden info (true_status, clue)  – only GameEngine may read these
  - public info (is_revealed, proven_status) – visible to Logic Agent
"""

from __future__ import annotations


class Card:
    """One character card on the board."""

    def __init__(
        self,
        cell_id: str,
        name: str,
        occupation: str,
        true_status: str,
        clue: dict,
    ) -> None:
        # ── identity ──
        self.cell_id: str = cell_id              # e.g. "A1"
        self.name: str = name                      # e.g. "Alice"
        self.occupation: str = occupation          # e.g. "Teacher"

        # ── hidden (only GameEngine) ──
        self.true_status: str = true_status        # "Criminal" or "Innocent"
        self.clue: dict = clue                     # structured clue dict

        # ── public ──
        self.is_revealed: bool = False             # face-up or face-down
        self.proven_status: str | None = None      # None / "Criminal" / "Innocent"

    # ────────────────────── helpers ──────────────────────────

    @property
    def col_letter(self) -> str:
        """Column letter extracted from cell_id, e.g. 'A' from 'A1'."""
        return self.cell_id[0]

    @property
    def row_number(self) -> int:
        """Row number extracted from cell_id, e.g. 1 from 'A1'."""
        return int(self.cell_id[1:])

    @property
    def grid_col(self) -> int:
        """Zero-based column index (A=0, B=1, ...)."""
        return ord(self.col_letter) - ord("A")

    @property
    def grid_row(self) -> int:
        """Zero-based row index."""
        return self.row_number - 1

    @property
    def is_criminal(self) -> bool:
        return self.true_status == "Criminal"

    @property
    def is_innocent(self) -> bool:
        return self.true_status == "Innocent"

    @property
    def is_solved(self) -> bool:
        return self.proven_status is not None

    def reveal(self) -> None:
        """Flip the card face-up and lock the proven status."""
        self.is_revealed = True
        self.proven_status = self.true_status

    def get_clue_text(self) -> str:
        """Return a human-readable string for this card's clue."""
        return clue_to_text(self.clue)

    def get_public_info(self) -> dict:
        """Return only the information visible to the Logic Agent."""
        info: dict = {
            "cell_id": self.cell_id,
            "name": self.name,
            "occupation": self.occupation,
            "is_revealed": self.is_revealed,
            "proven_status": self.proven_status,
        }
        if self.is_revealed:
            info["clue"] = self.clue
        return info

    def __repr__(self) -> str:
        status = self.proven_status or "?"
        rev = "↑" if self.is_revealed else "↓"
        return f"Card({self.cell_id} {self.name} [{status}] {rev})"


# ────────────────────── clue → human-readable text ──────────────────────

def _region_label(region) -> str:
    """Convert a region specifier to readable Vietnamese text."""
    if isinstance(region, list):
        return ", ".join(region)
    if isinstance(region, str):
        if region.startswith("row_"):
            return f"Hàng {region[4:]}"
        if region.startswith("col_"):
            return f"Cột {region[4:]}"
        if region.startswith("neighbors_"):
            return f"các ô xung quanh {region[10:]}"
        if region.startswith("diagonal_"):
            return f"đường chéo {region[9:]}"
    return str(region)


def clue_to_text(clue: dict) -> str:
    """Convert a structured clue dict to a natural-language string."""
    if not clue:
        return ""

    # Ưu tiên lấy chuỗi text tiếng Việt có sẵn trong JSON
    if "text" in clue and clue["text"]:
        return clue["text"]

    ctype = clue.get("type", "")
    args = clue.get("args", {})

    if ctype == "FACT":
        return f"{args['person']} là {args['status']}."

    if ctype == "SAME":
        return f"{args['person1']} và {args['person2']} có cùng trạng thái."

    if ctype == "DIFFERENT":
        return f"{args['person1']} và {args['person2']} có trạng thái khác nhau."

    if ctype == "EXACTLY":
        region = _region_label(args.get("region", ""))
        return f"{region} có đúng {args.get('count', 0)} Tội phạm."

    if ctype == "AT_LEAST":
        region = _region_label(args.get("region", ""))
        return f"{region} có ít nhất {args.get('count', 0)} Tội phạm."

    if ctype == "AT_MOST":
        region = _region_label(args.get("region", ""))
        return f"{region} có nhiều nhất {args.get('count', 0)} Tội phạm."

    # ── extension clues ──
    if ctype == "NEIGHBOR_COUNT":
        return f"Ô {args.get('cell', '')} có đúng {args.get('count', 0)} Tội phạm xung quanh."

    if ctype == "DIAGONAL":
        direction = "chính" if args.get("direction") == "main" else "phụ"
        return f"Đường chéo {direction} có đúng {args.get('count', 0)} Tội phạm."

    return f"[{ctype}] {args}"