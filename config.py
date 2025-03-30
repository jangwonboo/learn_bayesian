import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Debug mode settings
DEBUG_MODE = os.getenv('DEBUG_MODE', 'False').lower() == 'true'
SHOW_COMMENTS = os.getenv('SHOW_COMMENTS', 'True').lower() == 'true'
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Logging configuration
LOGGING_CONFIG = {
    'enabled': os.getenv('LOGGING_ENABLED', 'True').lower() == 'true',
    'file_logging': os.getenv('FILE_LOGGING', 'True').lower() == 'true',
    'console_logging': os.getenv('CONSOLE_LOGGING', 'True').lower() == 'true'
}

# Code block visibility settings
CODE_BLOCKS = {
    'show_logging': os.getenv('SHOW_LOGGING_CODE', 'True').lower() == 'true',
    'show_comments': os.getenv('SHOW_CODE_COMMENTS', 'True').lower() == 'true',
    'show_debug_code': os.getenv('SHOW_DEBUG_CODE', 'True').lower() == 'true',
    'show_visualization_code': os.getenv('SHOW_VISUALIZATION_CODE', 'True').lower() == 'true'
}

# Conditional compilation decorator
def conditional_block(block_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if CODE_BLOCKS.get(block_name, True):
                return func(*args, **kwargs)
            return None
        return wrapper
    return decorator 