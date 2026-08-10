"""
GUI constants: colors, fonts, sizes, screen dimensions.
"""

# ──────────────────────────── Screen ────────────────────────────
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
FPS = 60
TITLE = "Griductive Solver"

# ──────────────────────────── Colors ────────────────────────────
# Base palette
BG_DARK = (18, 18, 30)
BG_PANEL = (28, 28, 48)
BG_CARD = (38, 42, 68)

# Card states
CARD_FACEDOWN = (45, 55, 95)
CARD_FACEDOWN_HOVER = (55, 68, 115)
CARD_CRIMINAL = (180, 40, 50)
CARD_CRIMINAL_LIGHT = (220, 60, 70)
CARD_INNOCENT = (30, 160, 80)
CARD_INNOCENT_LIGHT = (40, 200, 100)

# Highlights
HIGHLIGHT_CLUE = (255, 200, 50, 150)       # golden highlight for clue-related cells
HIGHLIGHT_HINT = (100, 180, 255, 150)       # blue highlight for hint
HIGHLIGHT_SELECTED = (255, 255, 100, 180)   # yellow for selected card

# Feedback
COLOR_ACCEPTED = (40, 200, 100)
COLOR_NOT_PROVABLE = (255, 200, 50)
COLOR_CONTRADICTED = (220, 50, 50)

# Text
TEXT_WHITE = (240, 240, 250)
TEXT_LIGHT = (200, 200, 220)
TEXT_DIM = (140, 140, 170)
TEXT_NAME = (255, 255, 255)
TEXT_OCCUPATION = (180, 180, 210)
TEXT_CLUE = (230, 230, 180)

# Buttons
BTN_PRIMARY = (60, 100, 200)
BTN_PRIMARY_HOVER = (80, 120, 230)
BTN_DANGER = (200, 50, 50)
BTN_DANGER_HOVER = (230, 70, 70)
BTN_SUCCESS = (40, 160, 80)
BTN_SUCCESS_HOVER = (50, 190, 100)
BTN_NEUTRAL = (70, 70, 100)
BTN_NEUTRAL_HOVER = (90, 90, 120)

# Menu
MENU_ACCENT = (100, 140, 255)
MENU_ACCENT_GLOW = (120, 160, 255, 80)

# Popup overlay
OVERLAY_COLOR = (0, 0, 0, 160)
POPUP_BG = (35, 35, 60)
POPUP_BORDER = (80, 100, 180)

# ──────────────────────────── Fonts ─────────────────────────────
FONT_FAMILY = None          # None = pygame default; set to path for custom font
FONT_SIZE_TITLE = 56
FONT_SIZE_HEADING = 36
FONT_SIZE_SUBTITLE = 28
FONT_SIZE_BODY = 20
FONT_SIZE_SMALL = 16
FONT_SIZE_TINY = 13
FONT_SIZE_CARD_NAME = 16
FONT_SIZE_CARD_OCCUPATION = 12
FONT_SIZE_CARD_STATUS = 14
FONT_SIZE_CARD_CLUE = 12

# ──────────────────────────── Layout ────────────────────────────
# Game scene layout
GRID_LEFT_MARGIN = 40
GRID_TOP_MARGIN = 60
GRID_LABEL_SIZE = 30          # row/column label size
CARD_PADDING = 8              # gap between cards
CONTROL_PANEL_WIDTH = 320     # right sidebar width
LOG_PANEL_HEIGHT = 250        # deduction log panel height

# Card sizes (will be computed dynamically based on grid size)
CARD_MIN_WIDTH = 90
CARD_MIN_HEIGHT = 100
CARD_MAX_WIDTH = 200
CARD_MAX_HEIGHT = 220
CARD_BORDER_RADIUS = 10

# Buttons
BTN_WIDTH = 140
BTN_HEIGHT = 42
BTN_RADIUS = 8
BTN_PADDING = 10

# Popup
POPUP_WIDTH = 360
POPUP_HEIGHT = 240

# ──────────────────────────── Animation ─────────────────────────
FLIP_DURATION_MS = 400        # card flip animation duration
FADE_DURATION_MS = 300        # fade in/out duration
HIGHLIGHT_PULSE_SPEED = 3.0   # highlight pulsing speed
FEEDBACK_DISPLAY_MS = 2000    # how long feedback message shows

# ──────────────────────────── Game ──────────────────────────────
VERDICT_CRIMINAL = "Criminal"
VERDICT_INNOCENT = "Innocent"
RESULT_ACCEPTED = "ACCEPTED"
RESULT_NOT_PROVABLE = "NOT_PROVABLE"
RESULT_CONTRADICTED = "CONTRADICTED"
STATUS_UNKNOWN = "UNKNOWN"
