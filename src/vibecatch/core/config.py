from ..styles import colors

# Vibe categories configuration
VIBE_CATEGORIES = {
    'happiness': {
        'name': 'Happiness and Joy',
        'description': 'Upbeat tempos and major keys activate the brain\'s reward system, releasing dopamine and serotonin.',
        'color': colors.GREEN
    },
    'emotional': {
        'name': 'Emotional Depth',
        'description': 'Minor keys and slower tempos evoke introspection and connection.',
        'color': colors.PINK
    },
    'relaxation': {
        'name': 'Relaxation and Calm',
        'description': 'Gentle rhythms and smooth harmonies help lower cortisol and activate the parasympathetic nervous system.',
        'color': colors.CYAN
    },
    'excitement': {
        'name': 'Excitement and Energy',
        'description': 'Fast-paced beats and dynamic rhythms increase physical and mental arousal.',
        'color': colors.ORANGE
    }
}

# Window configuration
WINDOW_MIN_WIDTH = 1200  # Increased from 1000
WINDOW_MIN_HEIGHT = 800  # Increased from 700
WINDOW_TITLE = "VibeCatch"

# Playlist widget configuration
PLAYLIST_MIN_WIDTH = 550  # Minimum width for each playlist widget
PLAYLIST_MIN_HEIGHT = 300  # Minimum height for each playlist widget

# Audio configuration
SAMPLE_RATE = 44100
BIT_DEPTH = 16
CHANNELS = 1
MAX_FILE_SIZE = 500 * 1000  # 500KB max for Shazam API
RECORD_TIME = 5  # seconds

# Layout configuration
LAYOUT_SPACING = 6
LAYOUT_MARGINS = 6
GRID_SPACING = 6

# API configuration
SHAZAM_API_HOST = "shazam-api6.p.rapidapi.com"
SHAZAM_API_KEY = "fa5a6a869emsha1e5c0d55e85365p18dc1djsnd0540648d450"
SHAZAM_API_ENDPOINT = "https://shazam-api6.p.rapidapi.com/shazam/recognize/"
