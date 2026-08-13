"""
Result Scene – displayed when the puzzle is solved.

Shows:
  - Win/Complete message
  - Statistics (time, moves, SAT calls, etc.)
  - Play Again / Back to Menu buttons
"""

from __future__ import annotations

import math
import time
from typing import Optional

import pygame

from game.game_engine import GameEngine
from gui.constants import *
from gui.widgets import Button, get_font, render_text


class ResultScene:
    """Victory / Result screen shown after puzzle completion."""

    def __init__(self, screen: pygame.Surface, engine: GameEngine) -> None:
        self.screen = screen
        self.engine = engine
        self.should_quit = False
        self.go_menu = False
        self.play_again = False

        self._start_time = time.time()

        # Stats
        self.stats = engine.get_stats()

        # Buttons
        cx = SCREEN_WIDTH // 2
        self.btn_again = Button(
            pygame.Rect(cx - 220, 630, 200, 48),
            "Play Again",
            BTN_PRIMARY, BTN_PRIMARY_HOVER,
            font_size=FONT_SIZE_BODY,
            border_radius=10,
        )
        self.btn_menu = Button(
            pygame.Rect(cx + 20, 630, 200, 48),
            "Main Menu",
            BTN_NEUTRAL, BTN_NEUTRAL_HOVER,
            font_size=FONT_SIZE_BODY,
            border_radius=10,
        )

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            self.should_quit = True
            return

        if self.btn_again.handle_event(event):
            self.play_again = True
        if self.btn_menu.handle_event(event):
            self.go_menu = True

    def update(self) -> None:
        pass

    def draw(self) -> None:
        t = time.time() - self._start_time
        self.screen.fill(BG_DARK)

        # Background celebration particles
        self._draw_confetti(t)

        cx = SCREEN_WIDTH // 2

        # ── Title ──
        pulse = int(4 * math.sin(t * 3))
        title_font = get_font(FONT_SIZE_TITLE, bold=True)
        title_surf = title_font.render("PUZZLE SOLVED!", True, COLOR_ACCEPTED)
        title_rect = title_surf.get_rect(centerx=cx, top=50 + pulse)
        self.screen.blit(title_surf, title_rect)

        # ── Puzzle name ──
        if self.engine.board:
            render_text(self.screen, self.engine.board.name,
                        cx, 125, TEXT_LIGHT, FONT_SIZE_HEADING,
                        center=True)

        # ── Stats box ──
        box_w, box_h = 520, 380  # Tăng chiều rộng & chiều cao để chống tràn
        box_x = cx - box_w // 2
        box_y = 175
        box_rect = pygame.Rect(box_x, box_y, box_w, box_h)
        pygame.draw.rect(self.screen, BG_PANEL, box_rect, border_radius=12)
        pygame.draw.rect(self.screen, POPUP_BORDER, box_rect, width=2, border_radius=12)

        # Stats content
        stats = self.stats
        y = box_y + 20
        line_h = 42  # Tối ưu khoảng cách dòng

        stat_items = [
            ("Thời gian",
             f"{int(stats.get('elapsed_time', 0)) // 60:02d}:"
             f"{int(stats.get('elapsed_time', 0)) % 60:02d}"),
            ("Số bước đi", str(stats.get("move_count", 0))),
            ("SAT calls", str(stats.get("total_sat_calls", 0))),
            ("Deduction steps", str(stats.get("deduction_steps", 0))),
            ("Primary vars", str(stats.get("primary_vars", "N/A"))),
            ("CNF clauses", str(stats.get("clauses", "N/A"))),
            ("Decisions", str(stats.get("total_decisions", 0))),
            ("Propagations", str(stats.get("total_propagations", 0))),
        ]

        val_font = get_font(FONT_SIZE_BODY, bold=True)
        
        for label, value in stat_items:
            # Nhãn bên trái
            render_text(self.screen, label, box_x + 25, y, TEXT_LIGHT, FONT_SIZE_BODY)
            
            # Giá trị căn lề phải chuẩn xác
            val_surf = val_font.render(str(value), True, TEXT_WHITE)
            val_rect = val_surf.get_rect(right=box_x + box_w - 25, top=y)
            self.screen.blit(val_surf, val_rect)

            y += line_h

        # ── Buttons ──
        self.btn_again.draw(self.screen)
        self.btn_menu.draw(self.screen)

    def _draw_confetti(self, t: float) -> None:
        """Draw floating celebration particles."""
        colors = [
            (255, 100, 100), (100, 255, 100), (100, 100, 255),
            (255, 255, 100), (255, 100, 255), (100, 255, 255),
        ]
        for i in range(30):
            x = int((i * 137 + t * 40 * ((i % 4) + 1)) % SCREEN_WIDTH)
            y = int((i * 89 + t * 25 * ((i % 3) + 1)) % SCREEN_HEIGHT)
            r = 3 + (i % 4)
            color = colors[i % len(colors)]
            alpha_color = tuple(c // 3 for c in color)
            pygame.draw.circle(self.screen, alpha_color, (x, y), r)