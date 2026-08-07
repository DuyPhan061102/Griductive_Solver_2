"""
Reusable UI widgets for the Pygame GUI.

Provides: Button, Popup, FeedbackToast, ScrollPanel, TextRenderer.
"""

from __future__ import annotations

import math
import time
from typing import Callable, List, Optional, Tuple

import pygame

from gui.constants import *


# ──────────────────────── Text Helpers ──────────────────────────

_font_cache: dict[Tuple, pygame.font.Font] = {}


def get_font(size: int, bold: bool = False) -> pygame.font.Font:
    """Get or create a cached font."""
    key = (size, bold)
    if key not in _font_cache:
        _font_cache[key] = pygame.font.SysFont("segoeui", size, bold=bold)
    return _font_cache[key]


def render_text(
    surface: pygame.Surface,
    text: str,
    x: int, y: int,
    color: Tuple = TEXT_WHITE,
    size: int = FONT_SIZE_BODY,
    bold: bool = False,
    center: bool = False,
    max_width: int = 0,
) -> int:
    """Render text to surface. Returns the height used."""
    font = get_font(size, bold)

    if max_width > 0:
        # Word-wrap
        words = text.split(" ")
        lines = []
        current = ""
        for word in words:
            test = f"{current} {word}".strip()
            if font.size(test)[0] > max_width and current:
                lines.append(current)
                current = word
            else:
                current = test
        if current:
            lines.append(current)

        total_h = 0
        for line in lines:
            surf = font.render(line, True, color)
            if center:
                rect = surf.get_rect(centerx=x, top=y + total_h)
            else:
                rect = surf.get_rect(topleft=(x, y + total_h))
            surface.blit(surf, rect)
            total_h += font.get_linesize()
        return total_h
    else:
        surf = font.render(text, True, color)
        if center:
            rect = surf.get_rect(centerx=x, top=y)
        else:
            rect = surf.get_rect(topleft=(x, y))
        surface.blit(surf, rect)
        return font.get_linesize()


# ──────────────────────── Button ────────────────────────────────

class Button:
    """Interactive button with hover effects."""

    def __init__(
        self,
        rect: pygame.Rect,
        text: str,
        color: Tuple = BTN_PRIMARY,
        hover_color: Tuple = BTN_PRIMARY_HOVER,
        text_color: Tuple = TEXT_WHITE,
        font_size: int = FONT_SIZE_BODY,
        border_radius: int = BTN_RADIUS,
        on_click: Optional[Callable] = None,
    ) -> None:
        self.rect = rect
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font_size = font_size
        self.border_radius = border_radius
        self.on_click = on_click
        self.hovered = False
        self.visible = True
        self.enabled = True

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle mouse events. Returns True if clicked."""
        if not self.visible or not self.enabled:
            return False

        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.on_click:
                    self.on_click()
                return True
        return False

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the button."""
        if not self.visible:
            return

        color = self.hover_color if self.hovered else self.color
        if not self.enabled:
            color = BTN_NEUTRAL

        pygame.draw.rect(surface, color, self.rect,
                         border_radius=self.border_radius)

        # Subtle border
        border_color = tuple(min(c + 30, 255) for c in color)
        pygame.draw.rect(surface, border_color, self.rect, width=1,
                         border_radius=self.border_radius)

        # Text
        font = get_font(self.font_size, bold=True)
        text_surf = font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)


# ──────────────────────── Popup / Dialog ────────────────────────

class Popup:
    """Modal popup dialog with title, message, and buttons."""

    def __init__(
        self,
        title: str,
        message: str = "",
        buttons: Optional[List[dict]] = None,
        width: int = POPUP_WIDTH,
        height: int = POPUP_HEIGHT,
    ) -> None:
        self.title = title
        self.message = message
        self.width = width
        self.height = height
        self.active = False
        self.result: Optional[str] = None

        # Position (centered on screen)
        self.x = (SCREEN_WIDTH - width) // 2
        self.y = (SCREEN_HEIGHT - height) // 2
        self.rect = pygame.Rect(self.x, self.y, width, height)

        # Create buttons
        self.buttons: List[Button] = []
        if buttons:
            btn_width = min(120, (width - 40) // len(buttons) - 10)
            btn_y = self.y + height - 60
            total_btn_width = len(buttons) * btn_width + (len(buttons) - 1) * 10
            btn_x = self.x + (width - total_btn_width) // 2

            for i, btn_info in enumerate(buttons):
                btn_rect = pygame.Rect(
                    btn_x + i * (btn_width + 10), btn_y,
                    btn_width, 40
                )
                value = btn_info.get("value", btn_info["text"])

                def make_callback(v=value):
                    def callback():
                        self.result = v
                        self.active = False
                    return callback

                self.buttons.append(Button(
                    rect=btn_rect,
                    text=btn_info["text"],
                    color=btn_info.get("color", BTN_PRIMARY),
                    hover_color=btn_info.get("hover_color", BTN_PRIMARY_HOVER),
                    on_click=make_callback(),
                ))

    def show(self) -> None:
        self.active = True
        self.result = None

    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        if not self.active:
            return None

        for btn in self.buttons:
            btn.handle_event(event)

        # Close on Escape
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.active = False
            self.result = "cancel"

        return self.result

    def draw(self, surface: pygame.Surface) -> None:
        if not self.active:
            return

        # Overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill(OVERLAY_COLOR)
        surface.blit(overlay, (0, 0))

        # Popup background
        pygame.draw.rect(surface, POPUP_BG, self.rect, border_radius=12)
        pygame.draw.rect(surface, POPUP_BORDER, self.rect, width=2,
                         border_radius=12)

        # Title
        render_text(surface, self.title,
                    self.x + self.width // 2, self.y + 20,
                    color=TEXT_WHITE, size=FONT_SIZE_SUBTITLE,
                    bold=True, center=True)

        # Message
        if self.message:
            render_text(surface, self.message,
                        self.x + self.width // 2, self.y + 65,
                        color=TEXT_LIGHT, size=FONT_SIZE_BODY,
                        center=True, max_width=self.width - 40)

        # Buttons
        for btn in self.buttons:
            btn.draw(surface)


# ──────────────────────── Feedback Toast ────────────────────────

class FeedbackToast:
    """Temporary feedback message that fades away."""

    def __init__(self) -> None:
        self.message: str = ""
        self.color: Tuple = COLOR_ACCEPTED
        self._show_time: float = 0
        self._duration: float = FEEDBACK_DISPLAY_MS / 1000.0
        self.active: bool = False

    def show(self, message: str, feedback_type: str = "ACCEPTED") -> None:
        self.message = message
        self.active = True
        self._show_time = time.time()

        if feedback_type == "ACCEPTED":
            self.color = COLOR_ACCEPTED
        elif feedback_type == "NOT_PROVABLE":
            self.color = COLOR_NOT_PROVABLE
        elif feedback_type == "CONTRADICTED":
            self.color = COLOR_CONTRADICTED
        else:
            self.color = TEXT_WHITE

    def update(self) -> None:
        if self.active and time.time() - self._show_time > self._duration:
            self.active = False

    def draw(self, surface: pygame.Surface) -> None:
        if not self.active:
            return

        elapsed = time.time() - self._show_time
        alpha = max(0, min(255, int(255 * (1.0 - elapsed / self._duration))))

        font = get_font(FONT_SIZE_BODY, bold=True)
        text_surf = font.render(self.message, True, self.color)

        # Background
        padding = 16
        bg_rect = pygame.Rect(
            SCREEN_WIDTH // 2 - text_surf.get_width() // 2 - padding,
            SCREEN_HEIGHT - 80,
            text_surf.get_width() + padding * 2,
            text_surf.get_height() + padding,
        )

        bg = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        bg.fill((*BG_PANEL, alpha))
        surface.blit(bg, bg_rect)

        # Border
        border_surf = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(border_surf, (*self.color, alpha), (0, 0, bg_rect.width, bg_rect.height),
                         width=2, border_radius=8)
        surface.blit(border_surf, bg_rect)

        # Text
        text_with_alpha = text_surf.copy()
        text_with_alpha.set_alpha(alpha)
        surface.blit(text_with_alpha,
                     (bg_rect.x + padding, bg_rect.y + padding // 2))


# ──────────────────────── Scroll Panel ──────────────────────────

class ScrollPanel:
    """Scrollable panel for deduction log display."""

    def __init__(self, rect: pygame.Rect) -> None:
        self.rect = rect
        self.lines: List[Tuple[str, Tuple]] = []  # (text, color)
        self.scroll_offset: int = 0
        self.line_height: int = 20
        self.max_visible: int = rect.height // self.line_height

    def add_line(self, text: str, color: Tuple = TEXT_LIGHT) -> None:
        self.lines.append((text, color))
        # Auto-scroll to bottom
        total = len(self.lines)
        if total > self.max_visible:
            self.scroll_offset = total - self.max_visible

    def clear(self) -> None:
        self.lines = []
        self.scroll_offset = 0

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEWHEEL and self.rect.collidepoint(pygame.mouse.get_pos()):
            self.scroll_offset = max(
                0,
                min(
                    self.scroll_offset - event.y,
                    max(0, len(self.lines) - self.max_visible),
                ),
            )

    def draw(self, surface: pygame.Surface) -> None:
        # Background
        pygame.draw.rect(surface, BG_PANEL, self.rect, border_radius=6)
        pygame.draw.rect(surface, (50, 50, 80), self.rect, width=1,
                         border_radius=6)

        # Clip
        clip = surface.get_clip()
        surface.set_clip(self.rect)

        font = get_font(FONT_SIZE_SMALL)
        y = self.rect.y + 4
        start = self.scroll_offset
        end = min(start + self.max_visible, len(self.lines))

        for i in range(start, end):
            text, color = self.lines[i]
            text_surf = font.render(text, True, color)
            surface.blit(text_surf, (self.rect.x + 8, y))
            y += self.line_height

        surface.set_clip(clip)

        # Scrollbar
        if len(self.lines) > self.max_visible:
            bar_h = max(20, self.rect.height * self.max_visible // len(self.lines))
            bar_y = self.rect.y + int(
                (self.rect.height - bar_h) * self.scroll_offset /
                max(1, len(self.lines) - self.max_visible)
            )
            pygame.draw.rect(surface, (80, 80, 120),
                             (self.rect.right - 8, bar_y, 6, bar_h),
                             border_radius=3)
