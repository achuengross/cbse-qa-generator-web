# config.py - CONFIGURATION SETTINGS
import os
from pathlib import Path

class Config:
    """Central configuration for CBSE Q&A Generator"""
    
    # APPLICATION INFO
    APP_NAME = "Engross Q&A Generator"
    APP_VERSION = "3.0"
    APP_DESCRIPTION = "CBSE Social Science Question & Answer Generator"
    
    # PATHS
    BASE_DIR = Path(__file__).parent
    DATA_DIR = BASE_DIR / "data" / "Processed_QA"
    MANIFESTS_DIR = BASE_DIR / "manifests"
    COMPONENTS_DIR = BASE_DIR / "components"
    ASSETS_DIR = BASE_DIR / "assets"
    
    # LOGO PATH
    LOGO_PATH = ASSETS_DIR / "engross_logo.png"
    
    # UI CONFIGURATION
    class UI:
        # WINDOW SETTINGS
        DEFAULT_GEOMETRY = "1200x800"
        MIN_WIDTH = 1000
        MIN_HEIGHT = 700
        
        
        # COLORS (Updated with your custom teal palette)
        COLORS = {
            "primary": "#5F99AE",        # Medium teal (predominant)
            "primary_dark": "#336D82",   # Dark teal
            "primary_light": "#7BB3C7",  # Lighter teal (computed)
            "secondary": "#F5ECE0",      # Light cream background
            "accent": "#693382",         # Purple accent
            "success": "#5F99AE",        # Use primary teal for success
            "warning": "#693382",        # Use purple for warnings
            "error": "#B8627D",          # Computed error color (purple-red mix)
            "surface": "#FFFFFF",        # White cards/surfaces
            "on_surface": "#2C2C2C",     # Dark text on white
            "divider": "#E0D5C7",        # Light divider (from secondary)
            "hover": "#7BB3C7",          # Lighter teal for hover
            "feature_highlight": "#F0F8FB"  # Very light teal highlight
        }
        
        # FONTS
        FONTS = {
            "header": ("Segoe UI", 20, "bold"),
            "subheader": ("Segoe UI", 16, "bold"),
            "title": ("Segoe UI", 14, "bold"),
            "body": ("Segoe UI", 11, "normal"),
            "small": ("Segoe UI", 10, "normal"),
            "button": ("Segoe UI", 11, "bold"),
            "tab": ("Segoe UI", 11, "normal")
        }
        
        # SPACING
        PADDING = {
            "small": 5,
            "medium": 10,
            "large": 20,
            "xlarge": 30
        }
    
    # QUESTION TYPES DISPLAY NAMES
    QUESTION_TYPE_NAMES = {
        "mcq": "Multiple Choice Questions",
        "assertion": "Assertion & Reasoning",
        "matching": "Matching Questions", 
        "chronology": "Chronology Questions",
        "visual": "Visual Questions",
        "very_short": "Very Short Answer",
        "short": "Short Answer", 
        "long": "Long Answer",
        "source": "Source-Based Questions",
        "competency": "Competency-Based Questions"
    }
    
    # QUESTION TYPE ICONS
    QUESTION_TYPE_ICONS = {
        "mcq": "🔤",
        "assertion": "⚖️", 
        "matching": "🔗",
        "chronology": "📅",
        "visual": "🖼️",
        "very_short": "✏️",
        "short": "📝",
        "long": "📋",
        "source": "📄",
        "competency": "🧠"
    }
    
    # SUBJECT CONFIGURATION
    SUBJECTS = {
        "Democratic_Politics": {
            "display_name": "Democratic Politics",
            "icon": "🏛️",
            "color": "#1976D2"
        },
        "Economics": {
            "display_name": "Economics", 
            "icon": "💰",
            "color": "#388E3C"
        },
        "Geography": {
            "display_name": "Geography",
            "icon": "🌍", 
            "color": "#F57C00"
        },
        "History": {
            "display_name": "History",
            "icon": "📚",
            "color": "#7B1FA2"
        }
    }
    
    # PRACTICE SESSION SETTINGS
    class Practice:
        DEFAULT_QUESTION_COUNT = 10
        MAX_QUESTION_COUNT = 50
        SHOW_PROGRESS = True
        RANDOMIZE_QUESTIONS = True
        SHOW_EXPLANATIONS = True
        AUTO_ADVANCE = False
        TIMER_ENABLED = False
        DEFAULT_TIMER_MINUTES = 30
    
    # WORKSHEET BUILDER SETTINGS  
    class WorksheetBuilder:
        DEFAULT_MARKS = 40
        SUPPORTED_FORMATS = ["txt", "docx"]
        DEFAULT_FORMAT = "docx"
        
        # Default question distributions
        TEMPLATES = {
            "20_marks": {
                "mcq": 4,
                "assertion": 3, 
                "matching": 1,
                "very_short": 4,
                "short": 2
            },
            "40_marks": {
                "mcq": 8,
                "assertion": 4,
                "matching": 2, 
                "very_short": 4,
                "short": 2,
                "long": 2
            },
            "80_marks": {
                "mcq": 16,
                "assertion": 8,
                "matching": 4,
                "chronology": 2,
                "very_short": 8, 
                "short": 4,
                "long": 4,
                "source": 2
            }
        }
    
    # FILE HANDLING
    class Files:
        ENCODING = "utf-8"
        FALLBACK_ENCODING = "latin-1"
        
        # Supported image formats for visual questions
        IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
        
        # Question file format
        QUESTION_BLOCK_START = "[QUESTION]"
        QUESTION_BLOCK_END = "---"
    
    # QUICK REVISION SETTINGS
    class QuickRevision:
        DEFAULT_QUESTIONS_PER_TYPE = 5
        MAX_QUESTIONS_PER_TYPE = 20
        SUPPORTED_QUESTION_TYPES = [
            "mcq", "assertion", "matching", "very_short", "short"
        ]
        MIXED_MODE_DEFAULT = True
    
    # LOGGING AND DEBUG
    class Debug:
        VERBOSE_LOADING = True
        SHOW_FILE_PATHS = False  
        LOG_ERRORS = True
        
    # EXPORT SETTINGS
    class Export:
        DEFAULT_FILENAME_FORMAT = "CBSE_Worksheet_{subject}_{date}"
        INCLUDE_ANSWER_KEY = True
        INCLUDE_MARKING_SCHEME = True
        
        # Word document settings
        WORD_FONT = "Calibri"
        WORD_FONT_SIZE = 11
        WORD_MARGINS = 1.0  # inches
        
        # Image settings for visual questions
        IMAGE_WIDTH_INCHES = 4.0
        IMAGE_MAX_HEIGHT_INCHES = 3.0
    
    # SYSTEM REQUIREMENTS
    class Requirements:
        PYTHON_MIN_VERSION = "3.8"
        REQUIRED_PACKAGES = [
            "tkinter",  # Usually built-in
            "Pillow",   # For image handling
            "python-docx"  # For Word export
        ]
        OPTIONAL_PACKAGES = [
            "openpyxl",  # For Excel export (future)
        ]

# Create global config instance
config = Config()

# Helper functions for easy access
def get_color(color_name: str) -> str:
    """Get color from theme"""
    return config.UI.COLORS.get(color_name, "#000000")

def get_font(font_name: str) -> tuple:
    """Get font tuple"""
    return config.UI.FONTS.get(font_name, ("Arial", 10, "normal"))

def get_padding(size: str) -> int:
    """Get padding size"""
    return config.UI.PADDING.get(size, 10)

def get_subject_info(subject: str) -> dict:
    """Get subject display information"""
    return config.SUBJECTS.get(subject, {
        "display_name": subject,
        "icon": "📖", 
        "color": "#666666"
    })

def get_question_type_display(q_type: str) -> str:
    """Get display name for question type"""
    return config.QUESTION_TYPE_NAMES.get(q_type, q_type.title())

def get_question_type_icon(q_type: str) -> str:
    """Get icon for question type"""
    return config.QUESTION_TYPE_ICONS.get(q_type, "❓")

# Validation functions
def validate_paths():
    """Validate that required directories exist"""
    required_dirs = [
        config.DATA_DIR,
        config.MANIFESTS_DIR, 
        config.COMPONENTS_DIR,
        config.ASSETS_DIR
    ]
    
    missing_dirs = []
    for directory in required_dirs:
        if not directory.exists():
            missing_dirs.append(str(directory))
    
    if missing_dirs:
        print(f"⚠️ Missing directories: {missing_dirs}")
        return False
    
    return True

def create_missing_directories():
    """Create missing directories"""
    directories = [
        config.DATA_DIR,
        config.MANIFESTS_DIR,
        config.COMPONENTS_DIR, 
        config.ASSETS_DIR
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")

# Initialize on import
if __name__ == "__main__":
    print(f"🔧 {config.APP_NAME} v{config.APP_VERSION}")
    print(f"📁 Base directory: {config.BASE_DIR}")
    
    if not validate_paths():
        print("🔨 Creating missing directories...")
        create_missing_directories()
        print("✅ Directory structure ready!")
    else:
        print("✅ All directories exist!")