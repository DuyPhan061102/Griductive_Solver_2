"""
Griductive Solver – Main Entry Point

A logic deduction game where players must identify Criminals and Innocents
based on revealed clues, using propositional logic and SAT solving.

Usage:
    python main.py
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pygame

from gui.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE, BG_DARK
from gui.menu import MenuScene
from gui.game_scene import GameScene
from gui.result_scene import ResultScene
from game.game_engine import GameEngine


class App:
    """Main application – manages scene transitions and game loop."""

    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption(TITLE)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        # Scenes
        self.current_scene = "menu"
        self.menu = MenuScene(self.screen)
        self.game_scene = None
        self.result_scene = None

        # Game engine (persistent across scene transitions)
        self.engine = GameEngine()

        # Remember selections for Play Again
        self._last_puzzle_path = None
        self._last_mode = "manual"

    def run(self) -> None:
        """Main game loop."""
        while self.running:
            dt = self.clock.tick(FPS)

            # ── Handle events ──
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break

                if self.current_scene == "menu":
                    self.menu.handle_event(event)
                elif self.current_scene == "game":
                    self.game_scene.handle_event(event)
                elif self.current_scene == "result":
                    self.result_scene.handle_event(event)

            # ── Update ──
            if self.current_scene == "menu":
                self.menu.update()
                if self.menu.should_quit:
                    self.running = False
                elif self.menu.chosen_puzzle:
                    self._start_game(
                        self.menu.chosen_puzzle,
                        self.menu.selected_mode,
                    )
                    self.menu.chosen_puzzle = None

            elif self.current_scene == "game":
                self.game_scene.update()
                if self.game_scene.should_quit:
                    self.running = False
                elif self.game_scene.go_back:
                    self._go_to_menu()
                elif self.game_scene.go_result:
                    self._go_to_result()

            elif self.current_scene == "result":
                self.result_scene.update()
                if self.result_scene.should_quit:
                    self.running = False
                elif self.result_scene.go_menu:
                    self._go_to_menu()
                elif self.result_scene.play_again:
                    self._play_again()

            # ── Draw ──
            if self.current_scene == "menu":
                self.menu.draw()
            elif self.current_scene == "game":
                self.game_scene.draw()
            elif self.current_scene == "result":
                self.result_scene.draw()

            pygame.display.flip()

        pygame.quit()

    def _start_game(self, puzzle_path: str, mode: str) -> None:
        """Load puzzle and transition to game scene."""
        self._last_puzzle_path = puzzle_path
        self._last_mode = mode

        self.engine = GameEngine()
        self.engine.load_puzzle(puzzle_path)

        self.game_scene = GameScene(self.screen, self.engine, mode)
        self.current_scene = "game"

        # If auto mode, start auto-solving immediately
        if mode == "auto":
            self.game_scene._auto_running = True
            self.game_scene.btn_auto.text = "⏸  Pause"
            self.game_scene.btn_auto.color = (200, 50, 50)
            self.game_scene.btn_auto.hover_color = (230, 70, 70)

    def _go_to_menu(self) -> None:
        """Return to menu."""
        self.menu = MenuScene(self.screen)
        self.current_scene = "menu"
        self.game_scene = None
        self.result_scene = None

    def _go_to_result(self) -> None:
        """Show result screen."""
        self.result_scene = ResultScene(self.screen, self.engine)
        self.current_scene = "result"

    def _play_again(self) -> None:
        """Restart the same puzzle."""
        if self._last_puzzle_path:
            self._start_game(self._last_puzzle_path, self._last_mode)


def main():
    app = App()
    app.run()


if __name__ == "__main__":
    main()
