from PyQt5.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, 
    QListWidget, QSizePolicy, QPushButton
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QClipboard, QGuiApplication

from ..styles import components

class PlaylistWidget(QFrame):
    def __init__(self, vibe_id, vibe_info):
        super().__init__()
        self.vibe_id = vibe_id
        self.vibe_info = vibe_info
        self.setup_ui()

    def setup_ui(self):
        """Initialize the UI components"""
        self.setStyleSheet(components.PLAYLIST_FRAME)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setSpacing(4)
        layout.setContentsMargins(6, 6, 6, 6)
        
        # Add header
        header = QFrame()
        header_layout = QHBoxLayout(header)
        header_layout.setSpacing(2)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        # Add title and description in a vertical layout
        title_section = QFrame()
        title_layout = QVBoxLayout(title_section)
        title_layout.setSpacing(2)
        title_layout.setContentsMargins(0, 0, 0, 0)
        
        # Add title
        title = QLabel(self.vibe_info['name'])
        title.setStyleSheet(components.PLAYLIST_TITLE(self.vibe_info['color']))
        title.setAlignment(Qt.AlignLeft)
        title_layout.addWidget(title)
        
        # Add description
        description = QLabel(self.vibe_info['description'])
        description.setStyleSheet(components.PLAYLIST_DESCRIPTION)
        description.setWordWrap(True)
        description.setAlignment(Qt.AlignLeft)
        title_layout.addWidget(description)
        
        header_layout.addWidget(title_section, stretch=1)
        
        # Add copy button
        copy_btn = QPushButton("📋")
        copy_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: #6272a4;
                font-size: 16px;
                padding: 4px;
            }
            QPushButton:hover {
                color: #8be9fd;
            }
        """)
        copy_btn.setToolTip("Copy song list")
        copy_btn.clicked.connect(self.copy_song_list)
        copy_btn.setFixedSize(24, 24)
        header_layout.addWidget(copy_btn)
        
        layout.addWidget(header)
        
        # Add song list
        self.song_list = QListWidget()
        self.song_list.setStyleSheet(components.SONG_LIST)
        self.song_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.song_list.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.song_list.setWordWrap(True)
        layout.addWidget(self.song_list)

    def add_song(self, title: str, artist: str) -> bool:
        """Add a song to the playlist"""
        item_text = f"{title} - {artist}"
        # Check if song already exists
        for i in range(self.song_list.count()):
            if self.song_list.item(i).text() == item_text:
                return False
        
        # Add new song
        self.song_list.addItem(item_text)
        # Ensure the new item is visible
        self.song_list.scrollToBottom()
        return True

    def copy_song_list(self):
        """Copy all songs to clipboard"""
        songs = []
        for i in range(self.song_list.count()):
            songs.append(self.song_list.item(i).text())
        
        if songs:
            text = f"{self.vibe_info['name']} Playlist:\n" + "\n".join(songs)
            clipboard = QGuiApplication.clipboard()
            clipboard.setText(text)

    def clear(self):
        """Clear all songs from the playlist"""
        self.song_list.clear()

    def get_songs(self):
        """Get all songs in the playlist"""
        songs = []
        for i in range(self.song_list.count()):
            songs.append(self.song_list.item(i).text())
        return songs
