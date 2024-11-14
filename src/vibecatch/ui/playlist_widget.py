from PyQt5.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, 
    QListWidget, QSizePolicy, QPushButton
)
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QClipboard, QGuiApplication

from ..styles import components
from ..core.config import PLAYLIST_MIN_WIDTH, PLAYLIST_MIN_HEIGHT

class PlaylistWidget(QFrame):
    def __init__(self, vibe_id, vibe_info):
        super().__init__()
        self.vibe_id = vibe_id
        self.vibe_info = vibe_info
        self.notification_timer = QTimer()
        self.notification_timer.timeout.connect(self.hide_notification)
        self.notification_timer.setSingleShot(True)
        self.setup_ui()

    def setup_ui(self):
        """Initialize the UI components"""
        self.setStyleSheet(components.PLAYLIST_FRAME)
        self.setMinimumSize(PLAYLIST_MIN_WIDTH, PLAYLIST_MIN_HEIGHT)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setSpacing(4)
        layout.setContentsMargins(6, 6, 6, 6)
        
        # Add header
        header = QFrame()
        header.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        header_layout = QHBoxLayout(header)
        header_layout.setSpacing(2)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        # Add title and description in a vertical layout
        title_section = QFrame()
        title_section.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        title_layout = QVBoxLayout(title_section)
        title_layout.setSpacing(2)
        title_layout.setContentsMargins(0, 0, 0, 0)
        
        # Add title
        title = QLabel(self.vibe_info['name'])
        title.setStyleSheet(components.PLAYLIST_TITLE(self.vibe_info['color']))
        title.setAlignment(Qt.AlignLeft)
        title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        title.setMinimumHeight(30)
        title_layout.addWidget(title)
        
        # Add description
        description = QLabel(self.vibe_info['description'])
        description.setStyleSheet(components.PLAYLIST_DESCRIPTION)
        description.setWordWrap(True)
        description.setAlignment(Qt.AlignLeft)
        description.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        description.setMinimumHeight(40)
        title_layout.addWidget(description)
        
        header_layout.addWidget(title_section, stretch=1)
        
        # Create copy section with button and notification
        copy_section = QFrame()
        copy_section.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        copy_layout = QHBoxLayout(copy_section)
        copy_layout.setSpacing(4)
        copy_layout.setContentsMargins(0, 0, 0, 0)
        
        # Add copy button
        self.copy_btn = QPushButton("Copy")
        self.copy_btn.setStyleSheet(components.COPY_BUTTON)
        self.copy_btn.setToolTip("Copy song list")
        self.copy_btn.clicked.connect(self.copy_song_list)
        self.copy_btn.setFixedSize(60, 30)
        copy_layout.addWidget(self.copy_btn)
        
        # Add notification label
        self.notification = QLabel()
        self.notification.setStyleSheet(components.COPY_NOTIFICATION)
        self.notification.setFixedWidth(80)
        self.notification.hide()
        copy_layout.addWidget(self.notification)
        
        header_layout.addWidget(copy_section)
        
        layout.addWidget(header)
        
        # Add song list
        self.song_list = QListWidget()
        self.song_list.setStyleSheet(components.SONG_LIST)
        self.song_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.song_list.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.song_list.setWordWrap(True)
        self.song_list.setMinimumHeight(150)
        layout.addWidget(self.song_list)

    def minimumSizeHint(self) -> QSize:
        """Override minimum size hint"""
        return QSize(PLAYLIST_MIN_WIDTH, PLAYLIST_MIN_HEIGHT)

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
        """Copy all songs to clipboard and show notification"""
        songs = []
        for i in range(self.song_list.count()):
            songs.append(self.song_list.item(i).text())
        
        if songs:
            text = f"{self.vibe_info['name']} Playlist:\n" + "\n".join(songs)
            clipboard = QGuiApplication.clipboard()
            clipboard.setText(text)
            
            # Show notification
            self.notification.setText("Playlist copied!")
            self.notification.show()
            
            # Start fade timer
            self.notification_timer.start(2000)  # Hide after 2 seconds

    def hide_notification(self):
        """Hide the copy notification"""
        self.notification.hide()

    def clear(self):
        """Clear all songs from the playlist"""
        self.song_list.clear()

    def get_songs(self):
        """Get all songs in the playlist"""
        songs = []
        for i in range(self.song_list.count()):
            songs.append(self.song_list.item(i).text())
        return songs
