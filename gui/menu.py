"""
Main Menu screen – select game mode, grid size, and level.
"""

from __future__ import annotations

import math
import os
import time
from typing import Optional, Tuple

import pygame

from gui.constants import *
from gui.widgets import Button, get_font, render_text


class MenuScene:
    """Main menu with mode, size, and level selection."""

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen

        # Selection state
        self.selected_mode: str = "manual"     # "manual" or "auto"
        self.selected_size: int = 3            # 3, 4, or 5
        self.selected_level: int = 1           # 1 or 2

        # Result: the chosen puzzle path, or None if still browsing
        self.chosen_puzzle: Optional[str] = None
        self.should_quit: bool = False

        # Animation
        self._start_time = time.time()

        # ── Build buttons ──
        cx = SCREEN_WIDTH // 2
        self.buttons: dict = {}

        # Mode buttons
        y_mode = 280
        self.buttons["manual"] = Button(
            pygame.Rect(cx - 160, y_mode, 150, 44),
            "Manual", BTN_PRIMARY, BTN_PRIMARY_HOVER,
        )
        self.buttons["auto"] = Button(
            pygame.Rect(cx + 10, y_mode, 150, 44),
            "Auto", BTN_NEUTRAL, BTN_NEUTRAL_HOVER,
        )

        # Size buttons
        y_size = 380
        sizes = [(3, "3×3"), (4, "4×4"), (5, "5×5")]
        for i, (size, label) in enumerate(sizes):
            x = cx - 190 + i * 135
            self.buttons[f"size_{size}"] = Button(
                pygame.Rect(x, y_size, 120, 44),
                label,
                BTN_PRIMARY if size == 3 else BTN_NEUTRAL,
                BTN_PRIMARY_HOVER if size == 3 else BTN_NEUTRAL_HOVER,
            )

        # Level buttons
        y_level = 480
        self.buttons["level_1"] = Button(
            pygame.Rect(cx - 160, y_level, 150, 44),
            "Level 1", BTN_PRIMARY, BTN_PRIMARY_HOVER,
        )
        self.buttons["level_2"] = Button(
            pygame.Rect(cx + 10, y_level, 150, 44),
            "Level 2", BTN_NEUTRAL, BTN_NEUTRAL_HOVER,
        )

        # Start button
        self.buttons["start"] = Button(
            pygame.Rect(cx - 100, 580, 200, 52),
            "START GAME",
            BTN_SUCCESS, BTN_SUCCESS_HOVER,
            font_size=FONT_SIZE_SUBTITLE,
            border_radius=12,
        )

        self._update_button_visuals()

    def _update_button_visuals(self) -> None:
        """Update button colors to reflect current selection."""
        # Mode
        for key in ("manual", "auto"):
            is_selected = (key == self.selected_mode)
            self.buttons[key].color = BTN_PRIMARY if is_selected else BTN_NEUTRAL
            self.buttons[key].hover_color = BTN_PRIMARY_HOVER if is_selected else BTN_NEUTRAL_HOVER

        # Size
        for size in (3, 4, 5):
            is_selected = (size == self.selected_size)
            k = f"size_{size}"
            self.buttons[k].color = BTN_PRIMARY if is_selected else BTN_NEUTRAL
            self.buttons[k].hover_color = BTN_PRIMARY_HOVER if is_selected else BTN_NEUTRAL_HOVER

        # Level
        for lvl in (1, 2):
            is_selected = (lvl == self.selected_level)
            k = f"level_{lvl}"
            self.buttons[k].color = BTN_PRIMARY if is_selected else BTN_NEUTRAL
            self.buttons[k].hover_color = BTN_PRIMARY_HOVER if is_selected else BTN_NEUTRAL_HOVER

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            self.should_quit = True
            return

        # Button clicks
        for key, btn in self.buttons.items():
            if btn.handle_event(event):
                if key == "manual":
                    self.selected_mode = "manual"
                elif key == "auto":
                    self.selected_mode = "auto"
                elif key.startswith("size_"):
                    self.selected_size = int(key.split("_")[1])
                elif key == "level_1":
                    self.selected_level = 1
                elif key == "level_2":
                    self.selected_level = 2
                elif key == "start":
                    self._start_game()

                self._update_button_visuals()

    def _start_game(self) -> None:
        """Determine the puzzle file path and signal transition."""
        # Build the puzzle file name
        filename = f"{self.selected_size}x{self.selected_size}_lv{self.selected_level}.json"
        puzzle_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "puzzles")
        path = os.path.join(puzzle_dir, filename)

        if os.path.exists(path):
            self.chosen_puzzle = path
        else:
            # Fallback: try relative
            self.chosen_puzzle = os.path.join("puzzles", filename)

    def update(self) -> None:
        """Update animations."""
        pass

    def draw(self) -> None:
        """Draw the menu screen."""
        t = time.time() - self._start_time

        # ── Background ──
        self.screen.fill(BG_DARK)

        # Animated background particles
        self._draw_particles(t)

        # ── Title ──
        # Glow effect
        glow_alpha = int(40 + 20 * math.sin(t * 2))
        title_font = get_font(FONT_SIZE_TITLE, bold=True)
        title_text = "GRIDUCTIVE SOLVER"

        # Shadow
        shadow_surf = title_font.render(title_text, True, (30, 40, 80))
        shadow_rect = shadow_surf.get_rect(centerx=SCREEN_WIDTH // 2 + 3,
                                           top=83)
        self.screen.blit(shadow_surf, shadow_rect)

        # Main title
        title_surf = title_font.render(title_text, True, MENU_ACCENT)
        title_rect = title_surf.get_rect(centerx=SCREEN_WIDTH // 2, top=80)
        self.screen.blit(title_surf, title_rect)

        # Subtitle
        render_text(self.screen, "A Logic Deduction Game",
                    SCREEN_WIDTH // 2, 150,
                    color=TEXT_DIM, size=FONT_SIZE_SUBTITLE, center=True)

        # ── Section Labels ──
        cx = SCREEN_WIDTH // 2

        render_text(self.screen, "Chế độ chơi",
                    cx, 248, color=TEXT_LIGHT, size=FONT_SIZE_BODY,
                    bold=True, center=True)

        render_text(self.screen, "Kích thước lưới",
                    cx, 348, color=TEXT_LIGHT, size=FONT_SIZE_BODY,
                    bold=True, center=True)

        render_text(self.screen, "Màn chơi",
                    cx, 448, color=TEXT_LIGHT, size=FONT_SIZE_BODY,
                    bold=True, center=True)

        # ── Buttons ──
        for btn in self.buttons.values():
            btn.draw(self.screen)

        # ── Puzzle info ──
        puzzle_names = {
            (3, 1): "Small Village",
            (3, 2): "Harbor Town",
            (4, 1): "City Square",
            (4, 2): "Night Market",
            (5, 1): "Grand Academy",
            (5, 2): "Royal Court",
        }
        name = puzzle_names.get(
            (self.selected_size, self.selected_level), "Unknown"
        )
        render_text(self.screen, f"Puzzle: {name}",
                    cx, 645, color=TEXT_DIM, size=FONT_SIZE_BODY, center=True)

        # ── Footer ──
        render_text(self.screen, "CSC14003 – Introduction to AI | Project 2",
                    cx, SCREEN_HEIGHT - 40,
                    color=TEXT_DIM, size=FONT_SIZE_SMALL, center=True)

    def _draw_particles(self, t: float) -> None:
        """Draw animated background particles for visual appeal."""
        for i in range(20):
            x = int((i * 173 + t * 15 * (i % 3 + 1)) % SCREEN_WIDTH)
            y = int((i * 97 + t * 8 * (i % 2 + 1)) % SCREEN_HEIGHT)
            r = 2 + (i % 3)
            alpha = 30 + int(20 * math.sin(t * 1.5 + i))
            color = (60 + i * 3, 80 + i * 2, 160 + i * 3)
            pygame.draw.circle(self.screen, color, (x, y), r)