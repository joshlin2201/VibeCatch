from PyQt5.QtWidgets import QFrame, QVBoxLayout, QPushButton, QProgressBar, QLabel, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSignal

from ..styles import components

class RecordWidget(QFrame):
    # Signals
    recording_started = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        """Initialize the UI components"""
        self.setStyleSheet(components.FRAME_BASE)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setSpacing(4)
        layout.setContentsMargins(6, 6, 6, 6)
        
        # Add record button
        self.record_button = QPushButton("Click to Start Listening")
        self.record_button.setStyleSheet(components.RECORD_BUTTON)
        self.record_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.record_button.clicked.connect(self.start_recording)
        layout.addWidget(self.record_button)
        
        # Add progress bar
        self.progress = QProgressBar()
        self.progress.setStyleSheet(components.PROGRESS_BAR)
        self.progress.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.progress.setMinimumHeight(20)
        self.progress.hide()
        layout.addWidget(self.progress)
        
        # Add status label
        self.status_label = QLabel()
        self.status_label.setStyleSheet(components.STATUS_LABEL)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)

        # Set fixed height for consistent layout
        self.setFixedHeight(120)

    def start_recording(self):
        """Start the recording process"""
        self.record_button.setEnabled(False)
        self.record_button.setText("Listening...")
        self.progress.setValue(0)
        self.progress.show()
        self.status_label.clear()
        self.recording_started.emit()

    def stop_recording(self):
        """Stop the recording process"""
        self.record_button.setEnabled(True)
        self.record_button.setText("Click to Start Listening")
        self.progress.hide()

    def update_progress(self, value: int):
        """Update the progress bar"""
        self.progress.setValue(value)

    def update_status(self, message: str):
        """Update the status label"""
        self.status_label.setText(message)
        # Ensure status is visible
        self.status_label.adjustSize()
