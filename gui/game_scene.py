"""
Game Scene – the main gameplay screen.

Displays:
  - N×N card grid with row/column labels
  - Control panel (Restart, Hint, Auto Solve, Back)
  - Timer + Move counter
  - Deduction log (for Auto Solve mode)
  - Verdict popup, feedback toast, clue highlighting
"""

from __future__ import annotations

import math
import time
from typing import Dict, List, Optional, Tuple

import pygame

from game.card import Card
from game.game_engine import GameEngine
from gui.constants import *
from gui.widgets import (Button, FeedbackToast, Popup, ScrollPanel,
                         get_font, render_text)


class GameScene:
    """Main gameplay screen with card grid and controls."""

    def __init__(self, screen: pygame.Surface, engine: GameEngine,
                 mode: str = "manual") -> None:
        self.screen = screen
        self.engine = engine
        self.mode = mode           # "manual" or "auto"

        # Navigation
        self.go_back: bool = False
        self.go_result: bool = False
        self.should_quit: bool = False

        # Card rendering
        self.card_rects: Dict[str, pygame.Rect] = {}    # cell_id -> rect
        self.card_width: int = 0
        self.card_height: int = 0
        self._compute_card_layout()

        # Interaction state
        self.selected_clue_owner: Optional[str] = None  # whose clue is highlighted
        self.highlighted_cells: List[str] = []
        self.hint_cell: Optional[str] = None

        # Card flip animation
        self._flip_card: Optional[str] = None
        self._flip_start: float = 0
        self._flip_duration: float = FLIP_DURATION_MS / 1000.0

        # Auto solve animation
        self._auto_solve_timer: float = 0
        self._auto_solve_delay: float = 1.0  # seconds between auto steps
        self._auto_running: bool = False

        # UI components
        self.feedback = FeedbackToast()
        self.verdict_popup = self._create_verdict_popup()
        self._popup_target: Optional[str] = None  # character being judged

        # Control buttons
        self._create_control_buttons()

        # Deduction log
        panel_x = SCREEN_WIDTH - CONTROL_PANEL_WIDTH + 10
        self.log_panel = ScrollPanel(
            pygame.Rect(panel_x, 480, CONTROL_PANEL_WIDTH - 20, LOG_PANEL_HEIGHT)
        )

        # Time tracking
        self._anim_time = time.time()

    # ──────────────────────── Layout ────────────────────────────

    def _compute_card_layout(self) -> None:
        """Compute card sizes and positions based on grid size."""
        if not self.engine.board:
            return

        n = self.engine.board.size
        grid_area_w = SCREEN_WIDTH - CONTROL_PANEL_WIDTH - GRID_LEFT_MARGIN * 2 - GRID_LABEL_SIZE
        grid_area_h = SCREEN_HEIGHT - GRID_TOP_MARGIN * 2 - GRID_LABEL_SIZE

        self.card_width = min(CARD_MAX_WIDTH, max(CARD_MIN_WIDTH,
                              (grid_area_w - CARD_PADDING * (n - 1)) // n))
        self.card_height = min(CARD_MAX_HEIGHT, max(CARD_MIN_HEIGHT,
                               (grid_area_h - CARD_PADDING * (n - 1)) // n))

        # Starting position
        total_w = n * self.card_width + (n - 1) * CARD_PADDING
        total_h = n * self.card_height + (n - 1) * CARD_PADDING
        start_x = GRID_LEFT_MARGIN + GRID_LABEL_SIZE + \
                  (grid_area_w - total_w) // 2
        start_y = GRID_TOP_MARGIN + GRID_LABEL_SIZE

        self.card_rects = {}
        for card in self.engine.board.cards:
            col, row = card.grid_col, card.grid_row
            x = start_x + col * (self.card_width + CARD_PADDING)
            y = start_y + row * (self.card_height + CARD_PADDING)
            self.card_rects[card.cell_id] = pygame.Rect(x, y,
                                                         self.card_width,
                                                         self.card_height)

        # Store grid origin for labels
        self._grid_start_x = start_x
        self._grid_start_y = start_y

    def _create_verdict_popup(self) -> Popup:
        return Popup(
            title="Phán quyết",
            message="Nhân vật này là Criminal hay Innocent?",
            buttons=[
                {"text": "Criminal", "value": "Criminal",
                 "color": BTN_DANGER, "hover_color": BTN_DANGER_HOVER},
                {"text": "Innocent", "value": "Innocent",
                 "color": BTN_SUCCESS, "hover_color": BTN_SUCCESS_HOVER},
            ],
            width=400, height=200,
        )

    def _create_control_buttons(self) -> None:
        panel_x = SCREEN_WIDTH - CONTROL_PANEL_WIDTH + 10
        btn_w = CONTROL_PANEL_WIDTH - 20
        btn_h = 40
        y = 200

        self.btn_restart = Button(
            pygame.Rect(panel_x, y, btn_w, btn_h),
            "Restart", BTN_NEUTRAL, BTN_NEUTRAL_HOVER,
        )
        self.btn_hint = Button(
            pygame.Rect(panel_x, y + 50, btn_w, btn_h),
            "Hint", BTN_PRIMARY, BTN_PRIMARY_HOVER,
        )
        self.btn_auto = Button(
            pygame.Rect(panel_x, y + 100, btn_w, btn_h),
            "Auto Solve", BTN_SUCCESS, BTN_SUCCESS_HOVER,
        )
        self.btn_back = Button(
            pygame.Rect(panel_x, y + 150, btn_w, btn_h),
            "Back", BTN_NEUTRAL, BTN_NEUTRAL_HOVER,
        )

        self.control_buttons = [
            self.btn_restart, self.btn_hint,
            self.btn_auto, self.btn_back,
        ]

    # ──────────────────────── Events ────────────────────────────

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            self.should_quit = True
            return

        # Popup takes priority
        if self.verdict_popup.active:
            result = self.verdict_popup.handle_event(event)
            if result and result != "cancel" and self._popup_target:
                self._submit_verdict(self._popup_target, result)
                self._popup_target = None
            return

        # Scroll panel
        self.log_panel.handle_event(event)

        # Control buttons
        for btn in self.control_buttons:
            btn.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check control button clicks
            if self.btn_restart.rect.collidepoint(event.pos):
                self._do_restart()
            elif self.btn_hint.rect.collidepoint(event.pos):
                self._do_hint()
            elif self.btn_auto.rect.collidepoint(event.pos):
                self._do_auto_toggle()
            elif self.btn_back.rect.collidepoint(event.pos):
                self.go_back = True
            else:
                # Check card clicks
                self._handle_card_click(event.pos)

        # Hover for control buttons
        if event.type == pygame.MOUSEMOTION:
            for btn in self.control_buttons:
                btn.hovered = btn.rect.collidepoint(event.pos)

    def _handle_card_click(self, pos: Tuple[int, int]) -> None:
        """Handle clicking on a card."""
        if not self.engine.board:
            return

        for card in self.engine.board.cards:
            rect = self.card_rects.get(card.cell_id)
            if rect and rect.collidepoint(pos):
                if card.is_revealed:
                    # Toggle clue highlight
                    if self.selected_clue_owner == card.name:
                        self.selected_clue_owner = None
                        self.highlighted_cells = []
                    else:
                        self.selected_clue_owner = card.name
                        self.highlighted_cells = \
                            self.engine.get_highlighted_cells(card.name)
                else:
                    # Open verdict popup (manual mode only)
                    if self.mode == "manual" and not self._auto_running:
                        self._popup_target = card.name
                        self.verdict_popup.message = \
                            f"{card.name} ({card.occupation}) là Criminal hay Innocent?"
                        self.verdict_popup.show()
                break

    def _submit_verdict(self, character: str, verdict: str) -> None:
        """Submit a verdict and handle the result."""
        result = self.engine.submit_verdict(character, verdict)

        if result == "ACCEPTED":
            # Start flip animation
            card = self.engine.board.get_card_by_name(character)
            if card:
                self._flip_card = card.cell_id
                self._flip_start = time.time()

            self.feedback.show(
                f"{character} là {verdict}!",
                "ACCEPTED",
            )
            self.log_panel.add_line(
                f"{character} -> {verdict}", COLOR_ACCEPTED,
            )

            # Clear highlight
            self.selected_clue_owner = None
            self.highlighted_cells = []
            self.hint_cell = None

            # Check win
            if self.engine.is_finished:
                self.go_result = True

        elif result == "NOT_PROVABLE":
            self.feedback.show(
                f"Chưa thể chứng minh {character}.",
                "NOT_PROVABLE",
            )
            self.log_panel.add_line(
                f"{character}: NOT PROVABLE", COLOR_NOT_PROVABLE,
            )

        elif result == "CONTRADICTED":
            msg = self.engine.last_feedback.get("message", "Contradicted!")
            self.feedback.show(f"{msg}", "CONTRADICTED")
            self.log_panel.add_line(
                f"{character}: CONTRADICTED", COLOR_CONTRADICTED,
            )

    # ──────────────────────── Control Actions ──────────────────

    def _do_restart(self) -> None:
        self.engine.restart()
        self.selected_clue_owner = None
        self.highlighted_cells = []
        self.hint_cell = None
        self._auto_running = False
        self.log_panel.clear()
        self.log_panel.add_line("Game restarted.", TEXT_LIGHT)
        self.feedback.show("Game đã được khởi động lại.", "ACCEPTED")

    def _do_hint(self) -> None:
        hint = self.engine.request_hint()
        if hint:
            card = self.engine.board.get_card_by_name(hint["character"])
            if card:
                self.hint_cell = card.cell_id
            self.feedback.show(
                f"Gợi ý: {hint['character']} có thể là {hint['verdict']}.",
                "ACCEPTED",
            )
            self.log_panel.add_line(
                f"Hint: {hint['character']} -> {hint['verdict']}",
                HIGHLIGHT_HINT[:3],
            )
        else:
            self.feedback.show("Không tìm thấy gợi ý.", "NOT_PROVABLE")

    def _do_auto_toggle(self) -> None:
        self._auto_running = not self._auto_running
        if self._auto_running:
            self.btn_auto.text = "Pause"
            self.btn_auto.color = BTN_DANGER
            self.btn_auto.hover_color = BTN_DANGER_HOVER
            self._auto_solve_timer = time.time()
            self.log_panel.add_line("Auto Solve started.", MENU_ACCENT)
        else:
            self.btn_auto.text = "Auto Solve"
            self.btn_auto.color = BTN_SUCCESS
            self.btn_auto.hover_color = BTN_SUCCESS_HOVER
            self.log_panel.add_line("Auto Solve paused.", TEXT_DIM)

    # ──────────────────────── Update ───────────────────────────

    def update(self) -> None:
        """Update animations and auto-solve."""
        self._anim_time = time.time()
        self.feedback.update()

        # Flip animation done?
        if self._flip_card:
            if time.time() - self._flip_start > self._flip_duration:
                self._flip_card = None

        # Auto solve
        if self._auto_running and not self.engine.is_finished:
            if time.time() - self._auto_solve_timer > self._auto_solve_delay:
                self._auto_solve_timer = time.time()
                result = self.engine.auto_solve_step()
                if result:
                    step = result["step"]
                    card = self.engine.board.get_card_by_name(result["character"])
                    if card:
                        self._flip_card = card.cell_id
                        self._flip_start = time.time()

                    self.log_panel.add_line(
                        f"Step {step.step_number}: {result['character']} -> "
                        f"{result['verdict']} "
                        f"(SAT calls: {step.sat_queries})",
                        COLOR_ACCEPTED,
                    )

                    if self.engine.is_finished:
                        self._auto_running = False
                        self.btn_auto.text = "Auto Solve"
                        self.btn_auto.color = BTN_SUCCESS
                        self.btn_auto.hover_color = BTN_SUCCESS_HOVER
                        self.log_panel.add_line(
                            "Puzzle solved!", COLOR_ACCEPTED,
                        )
                        self.go_result = True
                else:
                    self._auto_running = False
                    self.btn_auto.text = "Auto Solve"
                    self.btn_auto.color = BTN_SUCCESS
                    self.btn_auto.hover_color = BTN_SUCCESS_HOVER
                    self.log_panel.add_line(
                        "No more provable verdicts.", COLOR_NOT_PROVABLE,
                    )

    # ──────────────────────── Drawing ──────────────────────────

    def draw(self) -> None:
        self.screen.fill(BG_DARK)

        if not self.engine.board:
            render_text(self.screen, "No puzzle loaded.",
                        SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                        center=True)
            return

        self._draw_grid_labels()
        self._draw_cards()
        self._draw_control_panel()
        self.log_panel.draw(self.screen)
        self.feedback.draw(self.screen)
        self.verdict_popup.draw(self.screen)

    def _draw_grid_labels(self) -> None:
        """Draw column letters and row numbers."""
        board = self.engine.board
        font = get_font(FONT_SIZE_BODY, bold=True)

        # Column labels
        for i, col in enumerate(board.columns):
            x = self._grid_start_x + i * (self.card_width + CARD_PADDING) + \
                self.card_width // 2
            y = self._grid_start_y - GRID_LABEL_SIZE
            surf = font.render(col, True, TEXT_DIM)
            rect = surf.get_rect(centerx=x, centery=y + GRID_LABEL_SIZE // 2)
            self.screen.blit(surf, rect)

        # Row labels
        for r in range(board.size):
            x = self._grid_start_x - GRID_LABEL_SIZE
            y = self._grid_start_y + r * (self.card_height + CARD_PADDING) + \
                self.card_height // 2
            surf = font.render(str(r + 1), True, TEXT_DIM)
            rect = surf.get_rect(centerx=x + GRID_LABEL_SIZE // 2, centery=y)
            self.screen.blit(surf, rect)

    def _draw_cards(self) -> None:
        """Draw all cards on the grid."""
        board = self.engine.board
        mouse_pos = pygame.mouse.get_pos()
        t = self._anim_time

        for card in board.cards:
            rect = self.card_rects.get(card.cell_id)
            if not rect:
                continue

            # Determine card state
            is_flipping = (self._flip_card == card.cell_id)
            is_highlighted = card.cell_id in self.highlighted_cells
            is_hint = (self.hint_cell == card.cell_id)
            is_hovered = rect.collidepoint(mouse_pos) and not self.verdict_popup.active

            # ── Flip animation ──
            draw_rect = rect
            if is_flipping:
                progress = (time.time() - self._flip_start) / self._flip_duration
                progress = min(1.0, progress)
                # Scale X for flip effect
                scale = abs(math.cos(progress * math.pi))
                new_w = max(4, int(rect.width * scale))
                draw_rect = pygame.Rect(
                    rect.centerx - new_w // 2, rect.y,
                    new_w, rect.height,
                )

            # ── Highlight glow ──
            if is_highlighted:
                pulse = int(20 * math.sin(t * HIGHLIGHT_PULSE_SPEED))
                glow_rect = rect.inflate(8 + pulse, 8 + pulse)
                glow_surf = pygame.Surface(
                    (glow_rect.width, glow_rect.height), pygame.SRCALPHA
                )
                glow_color = HIGHLIGHT_CLUE
                pygame.draw.rect(glow_surf, glow_color,
                                 (0, 0, glow_rect.width, glow_rect.height),
                                 border_radius=CARD_BORDER_RADIUS + 4)
                self.screen.blit(glow_surf, glow_rect)

            if is_hint:
                pulse = int(15 * math.sin(t * 4))
                glow_rect = rect.inflate(6 + pulse, 6 + pulse)
                glow_surf = pygame.Surface(
                    (glow_rect.width, glow_rect.height), pygame.SRCALPHA
                )
                pygame.draw.rect(glow_surf, HIGHLIGHT_HINT,
                                 (0, 0, glow_rect.width, glow_rect.height),
                                 border_radius=CARD_BORDER_RADIUS + 4)
                self.screen.blit(glow_surf, glow_rect)

            # ── Card background ──
            if card.is_revealed:
                if card.proven_status == "Criminal":
                    bg = CARD_CRIMINAL_LIGHT if is_hovered else CARD_CRIMINAL
                else:
                    bg = CARD_INNOCENT_LIGHT if is_hovered else CARD_INNOCENT
            else:
                bg = CARD_FACEDOWN_HOVER if is_hovered else CARD_FACEDOWN

            pygame.draw.rect(self.screen, bg, draw_rect,
                             border_radius=CARD_BORDER_RADIUS)

            # Border
            border_color = (255, 255, 255, 40) if is_hovered else (80, 80, 120)
            pygame.draw.rect(self.screen, border_color, draw_rect, width=2,
                             border_radius=CARD_BORDER_RADIUS)

            # ── Card content ──
            if draw_rect.width > 20:  # Only draw text if not too narrow (flip animation)
                self._draw_card_content(card, draw_rect)

    def _draw_card_content(self, card: Card, rect: pygame.Rect) -> None:
        """Draw the content of a single card."""
        cx = rect.centerx
        y = rect.y + 8
        max_w = rect.width - 12

        # Name (always shown)
        y += render_text(self.screen, card.name,
                         cx, y, TEXT_NAME, FONT_SIZE_CARD_NAME,
                         bold=True, center=True, max_width=max_w)

        # Occupation
        y += render_text(self.screen, card.occupation,
                         cx, y, TEXT_OCCUPATION, FONT_SIZE_CARD_OCCUPATION,
                         center=True, max_width=max_w)
        y += 4

        if card.is_revealed:
            # Status badge
            status_text = card.proven_status
            badge_font = get_font(FONT_SIZE_CARD_STATUS, bold=True)
            badge_surf = badge_font.render(
                f"{status_text}",
                True, TEXT_WHITE,
            )
            badge_rect = badge_surf.get_rect(centerx=cx, top=y)
            self.screen.blit(badge_surf, badge_rect)
            y += badge_font.get_linesize() + 4

            # Clue text
            clue_text = card.get_clue_text()
            render_text(self.screen, clue_text,
                        cx, y, TEXT_CLUE, FONT_SIZE_CARD_CLUE,
                        center=True, max_width=max_w)
        else:
            # Face-down indicator
            y += 8
            render_text(self.screen, "?",
                        cx, y, TEXT_DIM, FONT_SIZE_HEADING,
                        center=True)

    def _draw_control_panel(self) -> None:
        """Draw the right-side control panel."""
        panel_x = SCREEN_WIDTH - CONTROL_PANEL_WIDTH
        panel_rect = pygame.Rect(panel_x, 0, CONTROL_PANEL_WIDTH, SCREEN_HEIGHT)
        pygame.draw.rect(self.screen, BG_PANEL, panel_rect)
        pygame.draw.line(self.screen, (50, 50, 80),
                         (panel_x, 0), (panel_x, SCREEN_HEIGHT), 2)

        # ── Puzzle name (Hạ tọa độ Y từ 15 -> 30 để tránh bị cắt viền) ──
        render_text(self.screen, self.engine.board.name,
                    panel_x + CONTROL_PANEL_WIDTH // 2, 30,
                    TEXT_WHITE, FONT_SIZE_SUBTITLE, bold=True, center=True)

        size = self.engine.board.size
        render_text(self.screen, f"{size}x{size} Grid",
                    panel_x + CONTROL_PANEL_WIDTH // 2, 60,
                    TEXT_DIM, FONT_SIZE_BODY, center=True)

        # ── Timer ──
        elapsed = self.engine.get_elapsed_time()
        minutes = int(elapsed) // 60
        seconds = int(elapsed) % 60
        time_text = f"Time: {minutes:02d}:{seconds:02d}"
        render_text(self.screen, time_text,
                    panel_x + 20, 95,
                    TEXT_LIGHT, FONT_SIZE_BODY)

        # ── Move counter ──
        moves_text = f"Bước: {self.engine.move_count}"
        render_text(self.screen, moves_text,
                    panel_x + 20, 125,
                    TEXT_LIGHT, FONT_SIZE_BODY)

        # ── Progress ──
        total = self.engine.board.total_cards
        revealed = self.engine.board.revealed_count
        progress_text = f"Progress: {revealed}/{total} cards"
        render_text(self.screen, progress_text,
                    panel_x + 20, 155,
                    TEXT_LIGHT, FONT_SIZE_BODY)

        # ── Control buttons ──
        for btn in self.control_buttons:
            btn.draw(self.screen)

        # ── Log label ──
        render_text(self.screen, "Deduction Log",
                    panel_x + CONTROL_PANEL_WIDTH // 2, 455,
                    TEXT_DIM, FONT_SIZE_BODY, bold=True, center=True)