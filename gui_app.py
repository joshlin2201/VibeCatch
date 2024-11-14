import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import json
import os
from vibecatch import VibeCatch

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setMinimumSize(1000, 600)
        self.setWindowTitle("VibeCatch")
        
        # Initialize VibeCatch
        self.vibecatch = VibeCatch()
        
        # Create main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        # Create header
        self.header = QFrame()
        self.header.setStyleSheet("""
            QFrame {
                background-color: #2c313c;
                border-radius: 10px;
            }
        """)
        self.header.setMaximumHeight(100)
        self.header_layout = QHBoxLayout(self.header)
        
        # Add logo/title
        self.title = QLabel("VibeCatch")
        self.title.setStyleSheet("""
            QLabel {
                color: #ff79c6;
                font-size: 32px;
                font-weight: bold;
            }
        """)
        self.header_layout.addWidget(self.title)
        
        # Add header to main layout
        self.layout.addWidget(self.header)
        
        # Create content area
        self.content = QFrame()
        self.content.setStyleSheet("""
            QFrame {
                background-color: #282a36;
                border-radius: 10px;
            }
        """)
        self.content_layout = QVBoxLayout(self.content)
        
        # Add record button
        self.record_button = QPushButton("Start Listening")
        self.record_button.setStyleSheet("""
            QPushButton {
                background-color: #50fa7b;
                border-radius: 20px;
                padding: 15px;
                font-size: 18px;
                font-weight: bold;
                color: #282a36;
            }
            QPushButton:hover {
                background-color: #5af78e;
            }
            QPushButton:pressed {
                background-color: #45e06b;
            }
            QPushButton:disabled {
                background-color: #44475a;
            }
        """)
        self.record_button.clicked.connect(self.start_recording)
        self.content_layout.addWidget(self.record_button)
        
        # Add progress bar
        self.progress = QProgressBar()
        self.progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #44475a;
                border-radius: 5px;
                text-align: center;
                color: #f8f8f2;
            }
            QProgressBar::chunk {
                background-color: #bd93f9;
                border-radius: 3px;
            }
        """)
        self.progress.hide()
        self.content_layout.addWidget(self.progress)
        
        # Add status label
        self.status_label = QLabel()
        self.status_label.setStyleSheet("color: #f8f8f2;")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.content_layout.addWidget(self.status_label)
        
        # Add playlist area
        self.playlist_area = QFrame()
        self.playlist_area.setStyleSheet("""
            QFrame {
                background-color: #44475a;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        self.playlist_layout = QVBoxLayout(self.playlist_area)
        
        # Add playlist widgets
        self.playlist_widgets = {}
        for playlist_id, name in [
            ('hyped', 'Get Hyped'),
            ('chill', 'Chill Vibes'),
            ('romantic', 'Romantic Feels'),
            ('focus', 'Focus Mode'),
            ('feelgood', 'Feel-Good Tunes')
        ]:
            playlist_frame = QFrame()
            playlist_frame.setStyleSheet("""
                QFrame {
                    background-color: #282a36;
                    border-radius: 5px;
                    margin: 5px;
                    padding: 10px;
                }
            """)
            playlist_layout = QVBoxLayout(playlist_frame)
            
            # Add playlist title
            title = QLabel(name)
            title.setStyleSheet("""
                QLabel {
                    color: #ff79c6;
                    font-size: 18px;
                    font-weight: bold;
                }
            """)
            playlist_layout.addWidget(title)
            
            # Add song list
            song_list = QListWidget()
            song_list.setStyleSheet("""
                QListWidget {
                    background-color: #44475a;
                    border-radius: 5px;
                    color: #f8f8f2;
                }
                QListWidget::item {
                    padding: 5px;
                }
                QListWidget::item:hover {
                    background-color: #6272a4;
                }
            """)
            playlist_layout.addWidget(song_list)
            
            self.playlist_widgets[playlist_id] = song_list
            self.playlist_layout.addWidget(playlist_frame)
        
        # Add playlist area to content
        self.content_layout.addWidget(self.playlist_area)
        
        # Add content to main layout
        self.layout.addWidget(self.content)
        
        # Load existing playlists
        self.load_playlists()
        
        # Set window style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1f29;
            }
        """)

    def load_playlists(self):
        """Load existing playlists from file"""
        if os.path.exists('playlists.json'):
            try:
                with open('playlists.json', 'r') as f:
                    playlists = json.load(f)
                    for playlist_id, songs in playlists.items():
                        if playlist_id in self.playlist_widgets:
                            for song in songs:
                                self.playlist_widgets[playlist_id].addItem(
                                    f"{song['title']} - {song['artist']}"
                                )
            except Exception as e:
                print(f"Error loading playlists: {e}")

    def start_recording(self):
        """Start the recording process"""
        self.record_button.setEnabled(False)
        self.record_button.setText("Listening...")
        self.progress.setValue(0)
        self.progress.show()
        
        # Start recording in a separate thread
        self.record_thread = RecordThread(self.vibecatch)
        self.record_thread.progress_updated.connect(self.update_progress)
        self.record_thread.status_updated.connect(self.update_status)
        self.record_thread.recording_finished.connect(self.handle_recording_finished)
        self.record_thread.start()

    def update_progress(self, value):
        """Update progress bar"""
        self.progress.setValue(value)

    def update_status(self, message):
        """Update status label"""
        self.status_label.setText(message)

    def handle_recording_finished(self, result):
        """Handle recording completion"""
        self.record_button.setEnabled(True)
        self.record_button.setText("Start Listening")
        self.progress.hide()
        
        if result and 'song' in result:
            song = result['song']
            self.show_playlist_dialog(song)
        else:
            self.status_label.setText("Couldn't recognize the song. Please try again.")

    def show_playlist_dialog(self, song):
        """Show dialog to select playlist"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Add to Playlist")
        dialog.setStyleSheet("""
            QDialog {
                background-color: #282a36;
            }
        """)
        
        layout = QVBoxLayout(dialog)
        
        # Add song info
        song_info = QLabel(f"{song['title']}\nby {song['artist']}")
        song_info.setStyleSheet("color: #f8f8f2; font-size: 16px;")
        song_info.setAlignment(Qt.AlignCenter)
        layout.addWidget(song_info)
        
        # Add playlist buttons
        for playlist_id, name in [
            ('hyped', 'Get Hyped'),
            ('chill', 'Chill Vibes'),
            ('romantic', 'Romantic Feels'),
            ('focus', 'Focus Mode'),
            ('feelgood', 'Feel-Good Tunes')
        ]:
            btn = QPushButton(name)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #50fa7b;
                    border-radius: 15px;
                    padding: 10px;
                    font-size: 14px;
                    color: #282a36;
                }
                QPushButton:hover {
                    background-color: #5af78e;
                }
            """)
            btn.clicked.connect(lambda checked, p=playlist_id: self.add_to_playlist(song, p, dialog))
            layout.addWidget(btn)
        
        dialog.exec_()

    def add_to_playlist(self, song, playlist_id, dialog):
        """Add song to selected playlist"""
        if self.vibecatch.add_to_playlist(song, playlist_id):
            self.playlist_widgets[playlist_id].addItem(f"{song['title']} - {song['artist']}")
            self.status_label.setText(f"Added to {playlist_id} playlist!")
        dialog.close()

class RecordThread(QThread):
    progress_updated = pyqtSignal(int)
    status_updated = pyqtSignal(str)
    recording_finished = pyqtSignal(dict)

    def __init__(self, vibecatch):
        QThread.__init__(self)
        self.vibecatch = vibecatch

    def run(self):
        """Run the recording process"""
        self.status_updated.emit("Initializing audio...")
        
        # Record audio
        audio_file = self.vibecatch.record_audio()
        if not audio_file:
            self.recording_finished.emit({'error': 'Recording failed'})
            return
        
        self.status_updated.emit("Processing audio...")
        
        # Recognize song
        song = self.vibecatch.recognize_song(audio_file)
        if song:
            self.recording_finished.emit({'song': song})
        else:
            self.recording_finished.emit({'error': 'Recognition failed'})

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
