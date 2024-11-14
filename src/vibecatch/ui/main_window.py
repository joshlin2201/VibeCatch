from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QGridLayout, 
    QFrame, QLabel, QDialog, QPushButton
)
from PyQt5.QtCore import Qt

from ..core.config import VIBE_CATEGORIES, WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT, WINDOW_TITLE
from ..styles import components
from .playlist_widget import PlaylistWidget
from .record_widget import RecordWidget

class AddToPlaylistDialog(QDialog):
    def __init__(self, song, parent=None):
        super().__init__(parent)
        self.song = song
        self.selected_playlist = None
        self.setup_ui()

    def setup_ui(self):
        """Initialize the UI components"""
        self.setWindowTitle("Add to Playlist")
        self.setMinimumWidth(350)
        self.setStyleSheet(components.DIALOG_STYLE)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(12, 12, 12, 12)
        
        # Add song info
        song_info = QLabel(f"'{self.song['title']}'\nby {self.song['artist']}")
        song_info.setStyleSheet(components.DIALOG_SONG_INFO)
        song_info.setAlignment(Qt.AlignCenter)
        layout.addWidget(song_info)
        
        # Add playlist buttons
        for vibe_id, vibe_info in VIBE_CATEGORIES.items():
            btn = QPushButton(vibe_info['name'])
            btn.setStyleSheet(components.DIALOG_BUTTON(vibe_info['color']))
            btn.clicked.connect(lambda checked, v=vibe_id: self.select_playlist(v))
            layout.addWidget(btn)

    def select_playlist(self, playlist_id):
        """Handle playlist selection"""
        self.selected_playlist = playlist_id
        self.accept()

class MainWindow(QMainWindow):
    def __init__(self, audio_manager):
        super().__init__()
        self.audio_manager = audio_manager
        self.setup_ui()
        self.load_playlists()

    def setup_ui(self):
        """Initialize the UI components"""
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self.setWindowTitle(WINDOW_TITLE)
        self.setStyleSheet(f"background-color: {components.colors.BACKGROUND};")
        
        # Create main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(6)
        main_layout.setContentsMargins(6, 6, 6, 6)
        
        # Create header
        header = QFrame()
        header.setStyleSheet(components.FRAME_BASE)
        header_layout = QVBoxLayout(header)
        header_layout.setSpacing(2)
        header_layout.setContentsMargins(6, 6, 6, 6)
        
        # Add title
        title = QLabel("VibeCatch")
        title.setStyleSheet(components.TITLE_STYLE)
        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title)
        
        # Add tagline
        tagline = QLabel("Unlock the Science of Music")
        tagline.setStyleSheet(components.TAGLINE_STYLE)
        tagline.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(tagline)
        
        # Add description
        description = QLabel(
            "Music moves us, shapes our emotions, and transforms our everyday moments. "
            "Science identifies four core 'vibes' that music evokes. At Vibe Catch, "
            "we've harnessed this research to revolutionize how you connect with music—making "
            "it easy to find the perfect vibe for any moment."
        )
        description.setStyleSheet(components.DESCRIPTION_STYLE)
        description.setWordWrap(True)
        description.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(description)
        
        main_layout.addWidget(header)
        
        # Add record widget
        self.record_widget = RecordWidget()
        self.record_widget.recording_started.connect(self.start_recording)
        main_layout.addWidget(self.record_widget)
        
        # Create playlists section
        playlists_section = QFrame()
        playlists_section.setStyleSheet(components.FRAME_BASE)
        playlists_layout = QGridLayout(playlists_section)
        playlists_layout.setSpacing(6)
        playlists_layout.setContentsMargins(6, 6, 6, 6)
        
        # Add playlist widgets in a 2x2 grid
        self.playlist_widgets = {}
        for i, (vibe_id, vibe_info) in enumerate(VIBE_CATEGORIES.items()):
            playlist = PlaylistWidget(vibe_id, vibe_info)
            self.playlist_widgets[vibe_id] = playlist
            row = i // 2
            col = i % 2
            playlists_layout.addWidget(playlist, row, col)
        
        main_layout.addWidget(playlists_section)

    def load_playlists(self):
        """Load existing playlists"""
        for vibe_id in VIBE_CATEGORIES:
            songs = self.audio_manager.get_playlist(vibe_id)
            for song in songs:
                self.playlist_widgets[vibe_id].add_song(song['title'], song['artist'])

    def start_recording(self):
        """Start the recording process"""
        # Reset status
        self.record_widget.update_status("")
        
        # Connect signals from audio manager
        self.audio_manager.progress_updated.connect(self.record_widget.update_progress)
        self.audio_manager.status_updated.connect(self.record_widget.update_status)
        self.audio_manager.recording_finished.connect(self.handle_recording_finished)
        
        # Start recording
        self.audio_manager.start_recording()

    def handle_recording_finished(self, result):
        """Handle recording completion"""
        # Disconnect signals
        self.audio_manager.progress_updated.disconnect(self.record_widget.update_progress)
        self.audio_manager.status_updated.disconnect(self.record_widget.update_status)
        self.audio_manager.recording_finished.disconnect(self.handle_recording_finished)
        
        # Reset record widget
        self.record_widget.stop_recording()
        
        if result and 'song' in result:
            song = result['song']
            self.show_playlist_dialog(song)
        else:
            self.record_widget.update_status("Couldn't recognize the song. Click to try again.")

    def show_playlist_dialog(self, song):
        """Show dialog to select playlist"""
        dialog = AddToPlaylistDialog(song, self)
        if dialog.exec_() == QDialog.Accepted and dialog.selected_playlist:
            playlist_id = dialog.selected_playlist
            # Update both the playlist widget and the audio manager's playlist
            if self.audio_manager.add_to_playlist(song, playlist_id):
                if self.playlist_widgets[playlist_id].add_song(song['title'], song['artist']):
                    self.record_widget.update_status(
                        f"Added '{song['title']}' to {VIBE_CATEGORIES[playlist_id]['name']}! "
                        "Click to record another song."
                    )
                else:
                    self.record_widget.update_status(
                        f"Song already exists in {VIBE_CATEGORIES[playlist_id]['name']}. "
                        "Click to record another song."
                    )
            else:
                self.record_widget.update_status("Error adding song. Click to try again.")
