from . import colors

# Common styles
FRAME_BASE = f"""
    background-color: {colors.CURRENT_LINE};
    border-radius: 6px;
    padding: 6px;
"""

# Header styles
TITLE_STYLE = f"""
    color: {colors.PINK};
    font-size: 32px;
    font-weight: bold;
    margin: 10px;
"""

TAGLINE_STYLE = f"""
    color: {colors.FOREGROUND};
    font-size: 20px;
    margin: 8px;
"""

DESCRIPTION_STYLE = f"""
    color: {colors.FOREGROUND};
    font-size: 14px;
    margin: 6px 12px;
    line-height: 1.4;
"""

# Button styles
RECORD_BUTTON = f"""
    QPushButton {{
        background-color: {colors.GREEN};
        border-radius: 8px;
        padding: 8px;
        font-size: 20px;
        font-weight: bold;
        color: {colors.CURRENT_LINE};
        min-height: 45px;
        margin: 6px;
    }}
    QPushButton:hover {{
        background-color: {colors.GREEN_HOVER};
    }}
    QPushButton:pressed {{
        background-color: {colors.GREEN_PRESSED};
    }}
    QPushButton:disabled {{
        background-color: {colors.DARKER};
    }}
"""

# Progress bar styles
PROGRESS_BAR = f"""
    QProgressBar {{
        border: 2px solid {colors.DARKER};
        border-radius: 6px;
        text-align: center;
        color: {colors.FOREGROUND};
        font-size: 14px;
        min-height: 20px;
        margin: 6px;
    }}
    QProgressBar::chunk {{
        background-color: {colors.PURPLE};
        border-radius: 4px;
    }}
"""

# Status label styles
STATUS_LABEL = f"""
    color: {colors.FOREGROUND};
    font-size: 16px;
    margin: 6px;
"""

# Playlist styles
PLAYLIST_FRAME = f"""
    background-color: {colors.DARKER};
    border-radius: 6px;
    padding: 6px;
    margin: 4px;
"""

PLAYLIST_TITLE = lambda color: f"""
    color: {color};
    font-size: 18px;
    font-weight: bold;
    margin: 4px;
"""

PLAYLIST_DESCRIPTION = f"""
    color: {colors.FOREGROUND};
    font-size: 13px;
    margin: 4px;
    line-height: 1.3;
"""

SONG_LIST = f"""
    QListWidget {{
        background-color: {colors.CURRENT_LINE};
        border-radius: 4px;
        color: {colors.FOREGROUND};
        font-size: 14px;
        padding: 4px;
        min-height: 80px;
        max-height: 150px;
        margin: 4px;
    }}
    QListWidget::item {{
        padding: 4px;
        border-radius: 2px;
        margin: 1px;
    }}
    QListWidget::item:hover {{
        background-color: {colors.DARKER};
    }}
"""

# Dialog styles
DIALOG_STYLE = f"""
    background-color: {colors.CURRENT_LINE};
    padding: 12px;
"""

DIALOG_SONG_INFO = f"""
    color: {colors.FOREGROUND};
    font-size: 18px;
    padding: 8px;
    margin: 8px;
"""

DIALOG_BUTTON = lambda color: f"""
    QPushButton {{
        background-color: {color};
        border-radius: 6px;
        padding: 8px;
        font-size: 16px;
        color: {colors.CURRENT_LINE};
        min-height: 35px;
        margin: 4px;
    }}
    QPushButton:hover {{
        opacity: 0.9;
    }}
"""

# Scroll bar styles
SCROLL_BAR = f"""
    QScrollBar:vertical {{
        border: none;
        background: {colors.CURRENT_LINE};
        width: 10px;
        margin: 10px 0;
        border-radius: 5px;
    }}
    QScrollBar::handle:vertical {{
        background: {colors.DARKER};
        min-height: 20px;
        border-radius: 5px;
    }}
    QScrollBar::handle:vertical:hover {{
        background: {colors.COMMENT};
    }}
"""
