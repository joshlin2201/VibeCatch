import sys
from PyQt5.QtWidgets import QApplication

from .core.audio_manager import AudioManager
from .ui.main_window import MainWindow

def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    
    # Initialize audio manager
    audio_manager = AudioManager()
    
    # Create and show main window
    window = MainWindow(audio_manager)
    window.show()
    
    # Start application event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
